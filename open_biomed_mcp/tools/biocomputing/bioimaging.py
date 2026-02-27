"""
生物成像 
用途: 用于医学图像分割和配准的综合工具 主要功能:

SegmentationTool类: 使用nnUNet进行医学图像分割，处理BRATS数据集，模态分离和分割可视化
ImageRegistrationTool类: 使用SimpleITK进行医学图像配准，支持刚性、仿射和可变形配准
便捷函数: 提供分割、配准、预处理和相似性度量的快速接口
"""
import logging
import os
import sys
import zipfile

import matplotlib
import requests

matplotlib.use("Agg")  # Use non-interactive backend
import nibabel as nib
import numpy as np
import SimpleITK as sitk
import torch
import torch.serialization

# 禁用 nnunet 的输出
import warnings
warnings.filterwarnings('ignore')
# 临时重定向 stdout 来抑制 nnunet 的 print 输出
from io import StringIO
_original_stdout = sys.stdout
sys.stdout = StringIO()
try:
    from nnunet.inference.predict import predict_from_folder
finally:
    sys.stdout = _original_stdout


# ============================================================================
# SEGMENTATION CLASS
# ============================================================================


class SegmentationTool:
    """
    使用nnUNet进行医学图像分割的综合工具。
    处理BRATS数据集处理、模态分割和分割可视化。
    """

    def __init__(self):
        """初始化SegmentationTool。"""
        self.supported_formats = [".nii", ".nii.gz"]
        logger.info("SegmentationTool initialized")

    def split_modalities(self, input_file, output_dir, case_name="BRAT"):
        """
        将4D NIfTI文件分割为nnUNet的单独模态文件
        参数:
            input_file: 4D NIfTI文件的路径
            output_dir: 保存分割文件的目录
            case_name: 病例的基本名称（默认：BRAT）
        返回值:
            output_dir: 包含分割模态文件的目录路径
        """
        os.makedirs(output_dir, exist_ok=True)

        # Load the 4D image
        print(f"Loading {input_file}...")
        img = nib.load(input_file)
        data = img.get_fdata()

        print(f"Image shape: {data.shape}")
        print("Expected shape: (X, Y, Z, 4) for 4 modalities")

        if len(data.shape) != 4:
            raise ValueError(f"Expected 4D image, got {len(data.shape)}D")

        if data.shape[3] != 4:
            raise ValueError(f"Expected 4 modalities, got {data.shape[3]}")

        # Split into separate files
        modalities = ["FLAIR", "T1w", "t1gd", "T2w"]

        for i, modality in enumerate(modalities):
            # Extract the modality data
            modality_data = data[:, :, :, i]

            # Create a new NIfTI image with the same header but 3D data
            modality_img = nib.Nifti1Image(modality_data, img.affine, img.header)

            # Save with the expected naming convention
            output_file = os.path.join(output_dir, f"{case_name}_{i:04d}.nii.gz")
            nib.save(modality_img, output_file)

            print(f"Saved {modality} modality to {output_file}")
            print(f"  Shape: {modality_data.shape}, Data type: {modality_data.dtype}")

        print(f"\nAll modalities saved to {output_dir}")
        return output_dir

    def prepare_input_for_nnunet(self, input_path, output_dir, case_name="BRAT"):
        """
        通过处理4D和预分割模态文件为nnUNet准备输入数据
        参数:
            input_path: 输入文件或目录的路径
            output_dir: 保存准备好的文件的目录
            case_name: 病例的基本名称（默认：BRAT）
        返回值:
            prepared_dir: 包含nnUNet就绪文件的目录路径
        """
        os.makedirs(output_dir, exist_ok=True)

        if os.path.isfile(input_path):
            # Single file - check if it's 4D
            if input_path.endswith((".nii", ".nii.gz")):
                try:
                    img = nib.load(input_path)
                    if len(img.shape) == 4 and img.shape[3] == 4:
                        print("4D NIfTI file detected, splitting modalities...")
                        return self.split_modalities(input_path, output_dir, case_name)
                    else:
                        print("Single 3D file detected, copying to output directory...")
                        # Copy single file with proper naming
                        output_file = os.path.join(output_dir, f"{case_name}_0000.nii.gz")
                        import shutil

                        shutil.copy2(input_path, output_file)
                        return output_dir
                except Exception as e:
                    print(f"Error reading file {input_path}: {e}")
                    raise
        elif os.path.isdir(input_path):
            # Directory - check if it already has split modalities
            files = [f for f in os.listdir(input_path) if f.endswith((".nii", ".nii.gz"))]

            if any(f.endswith("_0000.nii.gz") for f in files):
                print("Directory already contains split modality files, using as-is...")
                # Copy existing files to output directory
                for f in files:
                    if f.endswith((".nii", ".nii.gz")):
                        import shutil

                        shutil.copy2(os.path.join(input_path, f), os.path.join(output_dir, f))
                return output_dir
            else:
                # Check if there's a 4D file to split
                for f in files:
                    if f.endswith((".nii", ".nii.gz")):
                        try:
                            img = nib.load(os.path.join(input_path, f))
                            if len(img.shape) == 4 and img.shape[3] == 4:
                                print(f"4D NIfTI file {f} detected, splitting modalities...")
                                return self.split_modalities(os.path.join(input_path, f), output_dir, case_name)
                        except Exception as e:
                            logging.debug("Skipping file %s during 4D check: %s", f, e)
                            continue

                print("No 4D files found, copying existing files...")
                # Copy existing files to output directory
                for f in files:
                    if f.endswith((".nii", ".nii.gz")):
                        import shutil

                        shutil.copy2(os.path.join(input_path, f), os.path.join(output_dir, f))
                return output_dir

        raise ValueError(f"Input path {input_path} is neither a valid file nor directory")

    def setup_nnunet_environment(self, results_folder=None, raw_data_base=None, preprocessed=None):
        """
        根据官方文档设置nnU-Net环境变量
        参数:
            results_folder: nnUNet结果文件夹的路径（默认：~/nnUNet_results）
            raw_data_base: 原始数据基础路径（默认：~/nnUNet_raw_data_base）
            preprocessed: 预处理数据路径（默认：~/nnUNet_preprocessed）
        """
        # Set nnUNet environment variables as per official documentation
        if results_folder:
            os.environ["nnUNet_RESULTS_FOLDER"] = os.path.expanduser(results_folder)
        elif "nnUNet_RESULTS_FOLDER" not in os.environ:
            os.environ["nnUNet_RESULTS_FOLDER"] = os.path.expanduser("~/nnUNet_results")

        if raw_data_base:
            os.environ["nnUNet_raw_data_base"] = os.path.expanduser(raw_data_base)
        elif "nnUNet_raw_data_base" not in os.environ:
            os.environ["nnUNet_raw_data_base"] = os.path.expanduser("~/nnUNet_raw_data_base")

        if preprocessed:
            os.environ["nnUNet_preprocessed"] = os.path.expanduser(preprocessed)
        elif "nnUNet_preprocessed" not in os.environ:
            os.environ["nnUNet_preprocessed"] = os.path.expanduser("~/nnUNet_preprocessed")

        # Create directories if they don't exist
        for path in [
            os.environ["nnUNet_RESULTS_FOLDER"],
            os.environ["nnUNet_raw_data_base"],
            os.environ["nnUNet_preprocessed"],
        ]:
            os.makedirs(path, exist_ok=True)

        print("nnU-Net environment variables set:")
        print(f"  nnUNet_RESULTS_FOLDER: {os.environ['nnUNet_RESULTS_FOLDER']}")
        print(f"  nnUNet_raw_data_base: {os.environ['nnUNet_raw_data_base']}")
        print(f"  nnUNet_preprocessed: {os.environ['nnUNet_preprocessed']}")

    def _download_model_with_browser_headers(self, url, output_path):
        """
        使用类浏览器头下载模型以绕过Zenodo的反机器人保护
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        logger.info(f"Downloading model from: {url}")

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=300)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"Download completed: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Download failed: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            return False

    def _download_and_extract_model(self, task_id, model_type="3d_fullres"):
        """
        使用类浏览器头下载并提取nnUNet模型 - 直接提取到nnUNet目录
        """
        results_folder = os.environ.get("nnUNet_RESULTS_FOLDER", "~/nnUNet_results")
        results_folder = os.path.expanduser(results_folder)

        # Create the nnUNet directory
        nnunet_dir = os.path.join(results_folder, "nnUNet")
        os.makedirs(nnunet_dir, exist_ok=True)

        # Check if model already exists
        task_dir = os.path.join(nnunet_dir, model_type, task_id)
        if os.path.exists(task_dir):
            # Check if it has the expected structure
            plans_file = os.path.join(task_dir, "nnUNetTrainerV2__nnUNetPlansv2.1")
            if os.path.exists(plans_file):
                logger.info(f"Model already exists for task '{task_id}' with {model_type}")
                return True

        # Download URL for the task
        download_url = f"https://zenodo.org/record/4003545/files/{task_id}.zip?download=1"

        # Create temporary file for download
        temp_zip = os.path.join(nnunet_dir, f"{task_id}_temp.zip")

        # Download with browser headers
        if self._download_model_with_browser_headers(download_url, temp_zip):
            try:
                logger.info(f"Extracting {temp_zip} to {nnunet_dir}")
                with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                    zip_ref.extractall(nnunet_dir)

                # Remove temporary zip file
                os.remove(temp_zip)

                # Verify extraction worked
                if os.path.exists(task_dir):
                    logger.info(f"Model successfully downloaded and extracted for task '{task_id}'")
                    logger.info(f"Model directory: {task_dir}")
                    return True
                else:
                    logger.error(f"Task directory not found after extraction: {task_dir}")
                    return False

            except Exception as e:
                logger.error(f"Extraction failed: {e}")
                if os.path.exists(temp_zip):
                    os.remove(temp_zip)
                return False
        else:
            return False

    def segment_with_nn_unet(
        self,
        image_path,
        output_dir,
        task_id,
        model_type="3d_fullres",
        folds=None,
        use_tta=False,
        num_threads=1,
        mixed_precision=True,
        verbose=True,
        auto_prepare_input=True,
        results_folder=None,
        auto_download=True,
    ):
        """
        使用nnUNet进行图像分割，具有适当的环境设置和自动模型下载
        参数:
            image_path: 输入图像文件或目录的路径
            output_dir: 保存分割结果的目录
            task_id: 任务标识符（例如'Task001_BrainTumour'）
            model_type: 模型类型（默认：'3d_fullres'）
            folds: 要使用的模型折叠（默认：[0, 1, 2, 3, 4]）
            use_tta: 使用测试时增强（默认：False）
            num_threads: 预处理的线程数（默认：1）
            mixed_precision: 使用混合精度（默认：True）
            verbose: 详细日志记录（默认：True）
            auto_prepare_input: 自动为nnUNet准备输入（默认：True）
            results_folder: nnUNet结果文件夹的路径（默认：None，将使用环境变量或默认值）
            auto_download: 自动下载缺失的模型（默认：True）
        """
        if folds is None:
            folds = [0, 1, 2, 3, 4]
        os.makedirs(output_dir, exist_ok=True)
        logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)

        # Setup nnUNet environment first
        self.setup_nnunet_environment(results_folder=results_folder)

        # Prepare input data if requested
        if auto_prepare_input:
            temp_input_dir = os.path.join(output_dir, "temp_input")
            prepared_input_dir = self.prepare_input_for_nnunet(image_path, temp_input_dir)
            image_path = prepared_input_dir
            logging.info(f"Input prepared for nnUNet: {image_path}")

        logging.info("Verifying NIfTI input files...")

        def verify_nifti_input(image_path):
            if os.path.isfile(image_path):
                nib.load(image_path)
            else:
                for file in os.listdir(image_path):
                    if file.endswith(".nii") or file.endswith(".nii.gz"):
                        nib.load(os.path.join(image_path, file))

        verify_nifti_input(image_path)

        # Get or set up the results folder
        results_folder = os.environ.get("nnUNet_RESULTS_FOLDER")
        if not results_folder:
            # Try common locations
            common_paths = [
                "./models/nnUNet",
                "~/nnUNet_results",
                "~/biomni_models/nnUNet",
            ]

            for base_path in common_paths:
                expanded_path = os.path.expanduser(base_path)
                if os.path.exists(expanded_path):
                    results_folder = expanded_path
                    break

            # If still no folder found, create one
            if not results_folder:
                results_folder = os.path.expanduser("~/nnUNet_results")
                os.makedirs(results_folder, exist_ok=True)
                logging.info(f"Created new results folder: {results_folder}")

        os.environ["RESULTS_FOLDER"] = results_folder
        os.environ["nnUNet_RESULTS_FOLDER"] = results_folder
        logging.info(f"Set RESULTS_FOLDER environment variable to: {results_folder}")

        # Construct the expected model path - using the correct structure
        model_folder = os.path.join(results_folder, "nnUNet", model_type, task_id, "nnUNetTrainerV2__nnUNetPlansv2.1")

        logging.info(f"Looking for model at: {model_folder}")

        # Check if model files actually exist (not just the directory)
        def check_model_files_exist(model_folder, folds):
            """Check if actual model weight files exist for the specified folds"""
            if not os.path.exists(model_folder):
                return False

            # Check for plans.pkl and other required files
            required_files = ["plans.pkl"]
            for req_file in required_files:
                if not os.path.exists(os.path.join(model_folder, req_file)):
                    return False

            # Check if at least one fold has model files
            for fold in folds:
                fold_dir = os.path.join(model_folder, f"fold_{fold}")
                if os.path.exists(fold_dir):
                    # Look for model files (.model, .model.pkl, etc.)
                    model_files = [f for f in os.listdir(fold_dir) if f.endswith((".model", ".model.pkl"))]
                    if model_files:
                        return True
            return False

        # Check if model exists, download if not
        if not check_model_files_exist(model_folder, folds):
            if auto_download:
                logging.info(f"Model weights for {task_id} not found. Downloading...")
                # Ensure the results folder structure exists
                os.makedirs(os.path.dirname(model_folder), exist_ok=True)

                # Download the model using our custom download function
                if self._download_and_extract_model(task_id, model_type):
                    logging.info(f"Downloaded pretrained model for {task_id} successfully.")
                else:
                    raise RuntimeError(f"Failed to download model for {task_id}")

                # Verify the download worked
                if not check_model_files_exist(model_folder, folds):
                    raise RuntimeError(
                        f"Model download completed but files not found at expected location: {model_folder}"
                    )
            else:
                # Ask user for permission to download
                user_input = (
                    input(f"Model weights for {task_id} not found. Do you want to download them? (y/n): ")
                    .strip()
                    .lower()
                )
                if user_input == "y":
                    # Download the model using our custom download function
                    if self._download_and_extract_model(task_id, model_type):
                        logging.info(f"Downloaded pretrained model for {task_id} successfully.")
                    else:
                        raise RuntimeError(f"Failed to download model for {task_id}")
                else:
                    raise RuntimeError("Model weights not found and download declined by user.")

        # Double-check that we now have the model
        if not check_model_files_exist(model_folder, folds):
            raise RuntimeError(f"Model files still not found at {model_folder} after download attempt")

        logging.info(f"Using model: {model_folder}")

        # Patch torch.load for compatibility
        original_torch_load = torch.load

        def patched_torch_load(*args, **kwargs):
            kwargs["weights_only"] = False
            return original_torch_load(*args, **kwargs)

        # Run the segmentation
        torch.load = patched_torch_load
        try:
            predict_from_folder(
                model=model_folder,
                input_folder=image_path,
                output_folder=output_dir,
                folds=folds,
                save_npz=False,
                num_threads_preprocessing=num_threads,
                num_threads_nifti_save=num_threads,
                mixed_precision=mixed_precision,
                lowres_segmentations=None,
                part_id=0,
                num_parts=1,
                tta=use_tta,
            )
        finally:
            # Restore original torch.load behavior
            torch.load = original_torch_load

        # Clean up temporary input directory if it was created
        if auto_prepare_input and os.path.exists(temp_input_dir):
            import shutil

            shutil.rmtree(temp_input_dir)
            logging.info("Cleaned up temporary input directory")

        logging.info(f"Segmentation outputs stored at: {output_dir}")
        return output_dir

    def create_segmentation_visualization(self, original_mri, segmentation, output_dir="./visualization_output"):
        """
        使用nilearn创建并保存分割结果的可视化
        参数:
            original_mri: 原始MRI文件的路径
            segmentation: 分割文件的路径
            output_dir: 保存可视化图像的目录
        返回值:
            list: 已保存图像文件路径的列表
        """
        try:
            # Import nilearn here to avoid dependency issues
            from nilearn import plotting

            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Check if files exist
            if not os.path.exists(original_mri):
                raise FileNotFoundError(f"Original MRI file not found: {original_mri}")

            if not os.path.exists(segmentation):
                raise FileNotFoundError(f"Segmentation file not found: {segmentation}")

            print("✅ Files found, creating visualizations...")
            saved_files = []

            # Create and save the main overlay plot
            display = plotting.plot_roi(
                segmentation,
                bg_img=original_mri,
                cmap="Set1",
                alpha=0.6,
                title="Segmentation Overlay",
            )

            # Save the main overlay plot
            output_file = os.path.join(output_dir, "segmentation_overlay.png")
            display.savefig(output_file, dpi=150, bbox_inches="tight")
            saved_files.append(output_file)
            print(f"✅ Main overlay saved to: {output_file}")
            display.close()

            # Create additional views and save them
            # Axial view
            display_axial = plotting.plot_roi(
                segmentation,
                bg_img=original_mri,
                cmap="Set1",
                alpha=0.6,
                title="Segmentation Overlay - Axial View",
                display_mode="z",
            )
            axial_file = os.path.join(output_dir, "segmentation_axial.png")
            display_axial.savefig(axial_file, dpi=150, bbox_inches="tight")
            saved_files.append(axial_file)
            print(f"✅ Axial view saved to: {axial_file}")
            display_axial.close()

            # Sagittal view
            display_sagittal = plotting.plot_roi(
                segmentation,
                bg_img=original_mri,
                cmap="Set1",
                alpha=0.6,
                title="Segmentation Overlay - Sagittal View",
                display_mode="x",
            )
            sagittal_file = os.path.join(output_dir, "segmentation_sagittal.png")
            display_sagittal.savefig(sagittal_file, dpi=150, bbox_inches="tight")
            saved_files.append(sagittal_file)
            print(f"✅ Sagittal view saved to: {sagittal_file}")
            display_sagittal.close()

            # Coronal view
            display_coronal = plotting.plot_roi(
                segmentation,
                bg_img=original_mri,
                cmap="Set1",
                alpha=0.6,
                title="Segmentation Overlay - Coronal View",
                display_mode="y",
            )
            coronal_file = os.path.join(output_dir, "segmentation_coronal.png")
            display_coronal.savefig(coronal_file, dpi=150, bbox_inches="tight")
            saved_files.append(coronal_file)
            print(f"✅ Coronal view saved to: {coronal_file}")
            display_coronal.close()

            print(f"\n✅ All visualizations saved to: {output_dir}")
            print("Files created:")
            for file_path in saved_files:
                print(f"  - {os.path.basename(file_path)}")

            return saved_files

        except ImportError:
            print(" nilearn not available. Install with: pip install nilearn")
            return []
        except Exception as e:
            print(f" Visualization failed: {e}")
            import traceback

            traceback.print_exc()
            return []


# ============================================================================
# IMAGE REGISTRATION CLASS
# ============================================================================


class ImageRegistrationTool:
    """
    使用SimpleITK进行医学图像配准的综合工具。
    支持刚性、仿射和可变形配准，具有预处理和可视化功能。
    """

    def __init__(self):
        """初始化ImageRegistrationTool。"""
        self.supported_formats = [".nii", ".nii.gz", ".nrrd", ".mha", ".mhd"]
        logger.info("ImageRegistrationTool initialized")

    def load_image(self, image_path: str) -> sitk.Image:
        """
        使用SimpleITK加载医学图像。

        参数:
            image_path: 图像文件的路径

        返回值:
            SimpleITK Image对象
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        logger.info(f"Loading image: {image_path}")
        try:
            image = sitk.ReadImage(image_path)
            logger.info(f"Successfully loaded image with size: {image.GetSize()}")
            return image
        except Exception as e:
            logger.error(f"Failed to load image {image_path}: {e}")
            raise

    def save_image(self, image: sitk.Image, output_path: str) -> None:
        """
        将SimpleITK图像保存到文件。

        参数:
            image: SimpleITK Image对象
            output_path: 保存图像的路径（必须包含文件名和扩展名）
        """
        # Validate output path
        if os.path.isdir(output_path):
            raise ValueError(
                f"Output path '{output_path}' is a directory. Please provide a file path with extension (e.g., '.nii.gz', '.png', '.jpg')"
            )

        if not os.path.splitext(output_path)[1]:
            raise ValueError(
                f"Output path '{output_path}' has no file extension. Please add an extension (e.g., '.nii.gz', '.png', '.jpg')"
            )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f"Saving image to: {output_path}")
        try:
            sitk.WriteImage(image, output_path)
            logger.info("Image saved successfully")
        except Exception as e:
            logger.error(f"Failed to save image to {output_path}: {e}")
            raise

    def preprocess_image(self, image: sitk.Image, denoise: bool = True, normalize: bool = True) -> sitk.Image:
        """
        使用去噪和归一化预处理图像。

        参数:
            image: 输入SimpleITK图像
            denoise: 是否应用去噪
            normalize: 是否应用归一化

        返回值:
            预处理后的SimpleITK图像
        """
        logger.info("Preprocessing image...")
        processed_image = sitk.Image(image)

        if denoise:
            # Apply Gaussian smoothing for denoising
            processed_image = sitk.SmoothingRecursiveGaussian(processed_image, sigma=1.0)
            logger.info("Applied denoising")

        if normalize:
            # Normalize to [0, 1] range
            min_max_filter = sitk.MinimumMaximumImageFilter()
            min_max_filter.Execute(processed_image)
            min_val = min_max_filter.GetMinimum()
            max_val = min_max_filter.GetMaximum()

            if max_val > min_val:
                processed_image = sitk.IntensityWindowing(
                    processed_image, windowMinimum=min_val, windowMaximum=max_val, outputMinimum=0.0, outputMaximum=1.0
                )
                logger.info("Applied normalization")

        return processed_image

    def create_rigid_transform(
        self, fixed_image: sitk.Image, moving_image: sitk.Image, initial_transform: sitk.Transform | None = None
    ) -> sitk.Transform:
        """
        为图像配准创建刚性变换。

        参数:
            fixed_image: 参考（固定）图像
            moving_image: 要配准的图像
            initial_transform: 可选的初始变换

        返回值:
            刚性变换对象
        """
        logger.info("Creating rigid transform...")

        if initial_transform is None:
            # Create identity transform
            transform = sitk.Euler3DTransform()
        else:
            transform = initial_transform

        return transform

    def create_affine_transform(
        self, fixed_image: sitk.Image, moving_image: sitk.Image, initial_transform: sitk.Transform | None = None
    ) -> sitk.Transform:
        """
        为图像配准创建仿射变换。

        参数:
            fixed_image: 参考（固定）图像
            moving_image: 要配准的图像
            initial_transform: 可选的初始变换

        返回值:
            仿射变换对象
        """
        logger.info("Creating affine transform...")

        if initial_transform is None:
            # Create identity transform
            transform = sitk.AffineTransform(3)
        else:
            transform = initial_transform

        return transform

    def create_deformable_transform(
        self, fixed_image: sitk.Image, moving_image: sitk.Image, number_of_control_points: int = 4
    ) -> sitk.Transform:
        """
        为图像配准创建可变形（B样条）变换。

        参数:
            fixed_image: 参考（固定）图像
            moving_image: 要配准的图像
            number_of_control_points: 每个维度的B样条控制点数量

        返回值:
            可变形变换对象
        """
        logger.info("Creating deformable transform...")

        # Create B-spline transform
        transform = sitk.BSplineTransformInitializer(fixed_image, [number_of_control_points] * 3, order=3)

        return transform

    def setup_registration_method(
        self,
        transform: sitk.Transform,
        metric: str = "mutual_information",
        optimizer: str = "gradient_descent",
        learning_rate: float = 0.01,
        number_of_iterations: int = 100,
        gradient_convergence_tolerance: float = 1e-6,
    ) -> sitk.ImageRegistrationMethod:
        """
        使用指定参数设置配准方法。

        参数:
            transform: 变换对象
            metric: 相似性度量名称
            optimizer: 优化器名称
            learning_rate: 梯度下降的学习率
            number_of_iterations: 最大迭代次数
            gradient_convergence_tolerance: 收敛容差

        返回值:
            配置好的配准方法
        """
        logger.info(f"Setting up registration method: {metric} metric, {optimizer} optimizer")

        registration_method = sitk.ImageRegistrationMethod()

        # Set similarity metric
        if metric == "mutual_information":
            registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
        elif metric == "mean_squares":
            registration_method.SetMetricAsMeanSquares()
        elif metric == "correlation":
            registration_method.SetMetricAsCorrelation()
        elif metric == "normalized_correlation":
            registration_method.SetMetricAsNormalizedCorrelation()
        else:
            logger.warning(f"Unknown metric {metric}, using mutual information")
            registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)

        # Set optimizer
        if optimizer == "gradient_descent":
            registration_method.SetOptimizerAsGradientDescent(
                learningRate=learning_rate,
                numberOfIterations=number_of_iterations,
                convergenceMinimumValue=gradient_convergence_tolerance,
            )
        elif optimizer == "lbfgsb":
            registration_method.SetOptimizerAsLBFGSB(
                gradientConvergenceTolerance=gradient_convergence_tolerance, numberOfIterations=number_of_iterations
            )
        elif optimizer == "powell":
            registration_method.SetOptimizerAsPowell(numberOfIterations=number_of_iterations, maximumLineIterations=20)
        elif optimizer == "amoeba":
            registration_method.SetOptimizerAsAmoeba(
                numberOfIterations=number_of_iterations, parametersConvergenceTolerance=gradient_convergence_tolerance
            )
        else:
            logger.warning(f"Unknown optimizer {optimizer}, using gradient descent")
            registration_method.SetOptimizerAsGradientDescent(
                learningRate=learning_rate,
                numberOfIterations=number_of_iterations,
                convergenceMinimumValue=gradient_convergence_tolerance,
            )

        # Set interpolator
        registration_method.SetInterpolator(sitk.sitkLinear)

        # Set initial transform
        registration_method.SetInitialTransform(transform, inPlace=False)

        return registration_method

    def register_images(
        self,
        fixed_image: sitk.Image,
        moving_image: sitk.Image,
        transform: sitk.Transform,
        registration_method: sitk.ImageRegistrationMethod,
    ) -> tuple[sitk.Transform, sitk.Image]:
        """
        执行图像配准。

        参数:
            fixed_image: 参考（固定）图像
            moving_image: 要配准的图像
            transform: 变换对象
            registration_method: 配置好的配准方法

        返回值:
            (final_transform, registered_image)的元组
        """
        logger.info("Starting image registration...")

        # Add iteration callback
        def command_iteration():
            logger.info(
                f"Iteration: {registration_method.GetOptimizerIteration()}, "
                f"Metric value: {registration_method.GetMetricValue():.6f}"
            )

        registration_method.AddCommand(sitk.sitkIterationEvent, command_iteration)

        try:
            # Execute registration
            final_transform = registration_method.Execute(fixed_image, moving_image)

            # Apply transform to moving image
            resampler = sitk.ResampleImageFilter()
            resampler.SetReferenceImage(fixed_image)
            resampler.SetInterpolator(sitk.sitkLinear)
            resampler.SetDefaultPixelValue(0)
            resampler.SetTransform(final_transform)

            registered_image = resampler.Execute(moving_image)

            logger.info("Registration completed successfully")
            return final_transform, registered_image

        except Exception as e:
            logger.error(f"Registration failed: {e}")
            raise

    def calculate_similarity_metrics(self, image1: sitk.Image, image2: sitk.Image) -> dict[str, float]:
        """
        计算两个图像之间的相似性度量。

        参数:
            image1: 第一个图像
            image2: 第二个图像

        返回值:
            相似性度量的字典
        """
        logger.info("Calculating similarity metrics...")
        metrics = {}

        try:
            # Convert to numpy arrays
            array1 = sitk.GetArrayFromImage(image1)
            array2 = sitk.GetArrayFromImage(image2)

            # Flatten arrays
            flat1 = array1.flatten()
            flat2 = array2.flatten()

            # Remove invalid values
            valid_mask = np.isfinite(flat1) & np.isfinite(flat2)
            flat1 = flat1[valid_mask]
            flat2 = flat2[valid_mask]

            if len(flat1) == 0:
                logger.warning("No valid pixels for similarity calculation")
                return {
                    "mutual_information": 0.0,
                    "mean_squares": 0.0,
                    "correlation": 0.0,
                    "normalized_correlation": 0.0,
                }

            # Mean Squared Error
            mse = np.mean((flat1 - flat2) ** 2)
            metrics["mean_squares"] = -mse  # Negative because we want to maximize

            # Pearson Correlation
            if np.std(flat1) > 0 and np.std(flat2) > 0:
                correlation = np.corrcoef(flat1, flat2)[0, 1]
                metrics["correlation"] = correlation if not np.isnan(correlation) else 0.0
            else:
                metrics["correlation"] = 0.0

            # Normalized Cross Correlation
            if np.std(flat1) > 0 and np.std(flat2) > 0:
                ncc = np.corrcoef(flat1, flat2)[0, 1]
                metrics["normalized_correlation"] = ncc if not np.isnan(ncc) else 0.0
            else:
                metrics["normalized_correlation"] = 0.0

            # Mutual Information (simplified calculation)
            try:
                # Create 2D histogram
                hist_2d, x_edges, y_edges = np.histogram2d(flat1, flat2, bins=50)
                hist_2d = hist_2d + 1e-10  # Add small value to avoid log(0)

                # Normalize histogram
                pxy = hist_2d / np.sum(hist_2d)
                px = np.sum(pxy, axis=1)
                py = np.sum(pxy, axis=0)

                # Calculate mutual information
                mi = 0.0
                for i in range(len(px)):
                    for j in range(len(py)):
                        if pxy[i, j] > 0 and px[i] > 0 and py[j] > 0:
                            mi += pxy[i, j] * np.log2(pxy[i, j] / (px[i] * py[j]))

                metrics["mutual_information"] = mi

            except Exception as e:
                logger.warning(f"Failed to calculate mutual information: {e}")
                metrics["mutual_information"] = 0.0

        except Exception as e:
            logger.warning(f"Failed to calculate similarity metrics: {e}")
            metrics = {
                "mutual_information": 0.0,
                "mean_squares": 0.0,
                "correlation": 0.0,
                "normalized_correlation": 0.0,
            }

        logger.info("Similarity metrics calculated")
        return metrics


# ============================================================================
# CONVENIENCE FUNCTIONS FOR BIOMNI INTEGRATION
# ============================================================================


# Segmentation convenience functions
def split_modalities(input_file, output_dir, case_name="BRAT"):
    """分割模态的便捷函数"""
    tool = SegmentationTool()
    return tool.split_modalities(input_file, output_dir, case_name)


def prepare_input_for_nnunet(input_path, output_dir, case_name="BRAT"):
    """准备nnUNet输入的便捷函数"""
    tool = SegmentationTool()
    return tool.prepare_input_for_nnunet(input_path, output_dir, case_name)


def segment_with_nn_unet(
    image_path,
    output_dir,
    task_id,
    model_type="3d_fullres",
    folds=None,
    use_tta=False,
    num_threads=1,
    mixed_precision=True,
    verbose=True,
    auto_prepare_input=True,
    results_folder=None,
):
    """nnUNet分割的便捷函数"""
    tool = SegmentationTool()
    return tool.segment_with_nn_unet(
        image_path,
        output_dir,
        task_id,
        model_type,
        folds,
        use_tta,
        num_threads,
        mixed_precision,
        verbose,
        auto_prepare_input,
        results_folder,
    )


def create_segmentation_visualization(original_mri, segmentation, output_dir="./visualization_output"):
    """分割可视化的便捷函数"""
    tool = SegmentationTool()
    return tool.create_segmentation_visualization(original_mri, segmentation, output_dir)


# Registration convenience functions
def preprocess_image(image_path: str, output_path: str, denoise: bool = True, normalize: bool = True) -> str:
    """
    用于Biomni集成的独立图像预处理函数。

    参数:
        image_path: 输入图像的路径
        output_path: 保存预处理图像的路径
        denoise: 是否应用去噪（默认：True）
        normalize: 是否应用归一化（默认：True）

    返回值:
        已保存预处理图像的路径
    """
    tool = ImageRegistrationTool()
    image = tool.load_image(image_path)
    preprocessed_image = tool.preprocess_image(image, denoise, normalize)
    tool.save_image(preprocessed_image, output_path)
    return output_path


def quick_rigid_registration(
    fixed_image_path: str,
    moving_image_path: str,
    output_dir: str,
    metric: str = "mutual_information",
    optimizer: str = "gradient_descent",
    preprocess: bool = True,
    create_visualizations: bool = True,
    learning_rate: float = 0.01,
    number_of_iterations: int = 100,
    gradient_convergence_tolerance: float = 1e-6,
) -> dict:
    """
    用于Biomni集成的快速刚性配准函数。

    参数:
        fixed_image_path: 参考图像的路径
        moving_image_path: 要配准的图像路径
        output_dir: 保存结果的目录
        metric: 相似性度量
        optimizer: 优化方法
        preprocess: 是否预处理图像
        create_visualizations: 是否创建可视化
        learning_rate: 优化器的学习率
        number_of_iterations: 最大迭代次数
        gradient_convergence_tolerance: 收敛容差

    返回值:
        包含配准结果的字典
    """
    tool = ImageRegistrationTool()

    # Load images
    fixed_image = tool.load_image(fixed_image_path)
    moving_image = tool.load_image(moving_image_path)

    # Preprocess if requested
    if preprocess:
        fixed_image = tool.preprocess_image(fixed_image)
        moving_image = tool.preprocess_image(moving_image)

    # Create transform and registration method
    transform = tool.create_rigid_transform(fixed_image, moving_image)
    registration_method = tool.setup_registration_method(
        transform, metric, optimizer, learning_rate, number_of_iterations, gradient_convergence_tolerance
    )

    # Perform registration
    final_transform, registered_image = tool.register_images(fixed_image, moving_image, transform, registration_method)

    # Save results
    os.makedirs(output_dir, exist_ok=True)

    # Save registered image
    registered_path = os.path.join(output_dir, "rigid_registered.nii.gz")
    tool.save_image(registered_image, registered_path)

    # Save transform
    transform_path = os.path.join(output_dir, "rigid_transform.tfm")
    sitk.WriteTransform(final_transform, transform_path)

    # Calculate metrics
    metrics_before = tool.calculate_similarity_metrics(fixed_image, moving_image)
    metrics_after = tool.calculate_similarity_metrics(fixed_image, registered_image)

    results = {
        "registered_image_path": registered_path,
        "transform_path": transform_path,
        "metrics_before": metrics_before,
        "metrics_after": metrics_after,
        "registration_type": "rigid",
    }

    return results


def quick_affine_registration(
    fixed_image_path: str,
    moving_image_path: str,
    output_dir: str,
    metric: str = "mutual_information",
    optimizer: str = "gradient_descent",
    preprocess: bool = True,
    create_visualizations: bool = True,
    learning_rate: float = 0.01,
    number_of_iterations: int = 100,
    gradient_convergence_tolerance: float = 1e-6,
) -> dict:
    """
    用于Biomni集成的快速仿射配准函数。

    参数:
        fixed_image_path: 参考图像的路径
        moving_image_path: 要配准的图像路径
        output_dir: 保存结果的目录
        metric: 相似性度量
        optimizer: 优化方法
        preprocess: 是否预处理图像
        create_visualizations: 是否创建可视化
        learning_rate: 优化器的学习率
        number_of_iterations: 最大迭代次数
        gradient_convergence_tolerance: 收敛容差

    返回值:
        包含配准结果的字典
    """
    tool = ImageRegistrationTool()

    # Load images
    fixed_image = tool.load_image(fixed_image_path)
    moving_image = tool.load_image(moving_image_path)

    # Preprocess if requested
    if preprocess:
        fixed_image = tool.preprocess_image(fixed_image)
        moving_image = tool.preprocess_image(moving_image)

    # Create transform and registration method
    transform = tool.create_affine_transform(fixed_image, moving_image)
    registration_method = tool.setup_registration_method(
        transform, metric, optimizer, learning_rate, number_of_iterations, gradient_convergence_tolerance
    )

    # Perform registration
    final_transform, registered_image = tool.register_images(fixed_image, moving_image, transform, registration_method)

    # Save results
    os.makedirs(output_dir, exist_ok=True)

    # Save registered image
    registered_path = os.path.join(output_dir, "affine_registered.nii.gz")
    tool.save_image(registered_image, registered_path)

    # Save transform
    transform_path = os.path.join(output_dir, "affine_transform.tfm")
    sitk.WriteTransform(final_transform, transform_path)

    # Calculate metrics
    metrics_before = tool.calculate_similarity_metrics(fixed_image, moving_image)
    metrics_after = tool.calculate_similarity_metrics(fixed_image, registered_image)

    results = {
        "registered_image_path": registered_path,
        "transform_path": transform_path,
        "metrics_before": metrics_before,
        "metrics_after": metrics_after,
        "registration_type": "affine",
    }

    return results


def quick_deformable_registration(
    fixed_image_path: str,
    moving_image_path: str,
    output_dir: str,
    metric: str = "mutual_information",
    optimizer: str = "gradient_descent",
    preprocess: bool = True,
    create_visualizations: bool = True,
    learning_rate: float = 0.01,
    number_of_iterations: int = 100,
    gradient_convergence_tolerance: float = 1e-6,
    number_of_control_points: int = 4,
) -> dict:
    """
    用于Biomni集成的快速可变形配准函数。

    参数:
        fixed_image_path: 参考图像的路径
        moving_image_path: 要配准的图像路径
        output_dir: 保存结果的目录
        metric: 相似性度量
        optimizer: 优化方法
        preprocess: 是否预处理图像
        create_visualizations: 是否创建可视化
        learning_rate: 优化器的学习率
        number_of_iterations: 最大迭代次数
        gradient_convergence_tolerance: 收敛容差
        number_of_control_points: B样条控制点数量

    返回值:
        包含配准结果的字典
    """
    tool = ImageRegistrationTool()

    # Load images
    fixed_image = tool.load_image(fixed_image_path)
    moving_image = tool.load_image(moving_image_path)

    # Preprocess if requested
    if preprocess:
        fixed_image = tool.preprocess_image(fixed_image)
        moving_image = tool.preprocess_image(moving_image)

    # Create transform and registration method
    transform = tool.create_deformable_transform(fixed_image, moving_image, number_of_control_points)
    registration_method = tool.setup_registration_method(
        transform, metric, optimizer, learning_rate, number_of_iterations, gradient_convergence_tolerance
    )

    # Perform registration
    final_transform, registered_image = tool.register_images(fixed_image, moving_image, transform, registration_method)

    # Save results
    os.makedirs(output_dir, exist_ok=True)

    # Save registered image
    registered_path = os.path.join(output_dir, "deformable_registered.nii.gz")
    tool.save_image(registered_image, registered_path)

    # Save transform
    transform_path = os.path.join(output_dir, "deformable_transform.tfm")
    sitk.WriteTransform(final_transform, transform_path)

    # Calculate metrics
    metrics_before = tool.calculate_similarity_metrics(fixed_image, moving_image)
    metrics_after = tool.calculate_similarity_metrics(fixed_image, registered_image)

    results = {
        "registered_image_path": registered_path,
        "transform_path": transform_path,
        "metrics_before": metrics_before,
        "metrics_after": metrics_after,
        "registration_type": "deformable",
    }

    return results


def batch_register_images(
    fixed_image_path: str,
    moving_images_dir: str,
    output_dir: str,
    transform_type: str = "rigid",
    metric: str = "mutual_information",
    optimizer: str = "gradient_descent",
    preprocess: bool = True,
    create_visualizations: bool = True,
    learning_rate: float = 0.01,
    number_of_iterations: int = 100,
    gradient_convergence_tolerance: float = 1e-6,
) -> dict:
    """
    将多个图像批量配准到单个参考图像。

    参数:
        fixed_image_path: 参考图像的路径
        moving_images_dir: 包含要配准图像的目录
        output_dir: 保存结果的目录
        transform_type: 配准类型（'rigid'、'affine'、'deformable'）
        metric: 相似性度量
        optimizer: 优化方法
        preprocess: 是否预处理图像
        create_visualizations: 是否创建可视化
        learning_rate: 优化器的学习率
        number_of_iterations: 最大迭代次数
        gradient_convergence_tolerance: 收敛容差

    返回值:
        包含批量配准结果的字典
    """
    logger.info(f"Starting batch {transform_type} registration...")

    # Find all image files in the directory
    image_files = []
    for file in os.listdir(moving_images_dir):
        if any(file.endswith(ext) for ext in [".nii", ".nii.gz", ".nrrd", ".mha", ".mhd"]):
            image_files.append(os.path.join(moving_images_dir, file))

    if not image_files:
        raise ValueError(f"No image files found in {moving_images_dir}")

    logger.info(f"Found {len(image_files)} images to register")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process each image
    results = {}
    ImageRegistrationTool()

    for i, moving_image_path in enumerate(image_files):
        logger.info(f"Processing {i + 1}/{len(image_files)}: {os.path.basename(moving_image_path)}")

        # Create individual output directory
        image_name = os.path.splitext(os.path.basename(moving_image_path))[0]
        if image_name.endswith(".nii"):
            image_name = os.path.splitext(image_name)[0]

        individual_output_dir = os.path.join(output_dir, f"registration_{image_name}")

        try:
            if transform_type == "rigid":
                result = quick_rigid_registration(
                    fixed_image_path,
                    moving_image_path,
                    individual_output_dir,
                    metric,
                    optimizer,
                    preprocess,
                    create_visualizations,
                    learning_rate,
                    number_of_iterations,
                    gradient_convergence_tolerance,
                )
            elif transform_type == "affine":
                result = quick_affine_registration(
                    fixed_image_path,
                    moving_image_path,
                    individual_output_dir,
                    metric,
                    optimizer,
                    preprocess,
                    create_visualizations,
                    learning_rate,
                    number_of_iterations,
                    gradient_convergence_tolerance,
                )
            elif transform_type == "deformable":
                result = quick_deformable_registration(
                    fixed_image_path,
                    moving_image_path,
                    individual_output_dir,
                    metric,
                    optimizer,
                    preprocess,
                    create_visualizations,
                    learning_rate,
                    number_of_iterations,
                    gradient_convergence_tolerance,
                )
            else:
                raise ValueError(f"Unknown transform type: {transform_type}")

            results[image_name] = result
            logger.info(f"Successfully registered {image_name}")

        except Exception as e:
            logger.error(f"Failed to register {image_name}: {e}")
            results[image_name] = {"error": str(e)}

    logger.info(f"Batch registration completed. Processed {len(image_files)} images.")
    return results


def calculate_similarity_metrics(image1_path: str, image2_path: str) -> dict[str, float]:
    """
    计算两个图像之间的相似性度量。

    参数:
        image1_path: 第一个图像的路径
        image2_path: 第二个图像的路径

    返回值:
        相似性度量的字典
    """
    tool = ImageRegistrationTool()
    image1 = tool.load_image(image1_path)
    image2 = tool.load_image(image2_path)
    return tool.calculate_similarity_metrics(image1, image2)

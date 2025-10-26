"""
Vision Analyzer - Multi-Modal Reasoning for Images
Analyzes screenshots, images, and visual content
LOCAL PROCESSING - Privacy-first approach
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import base64
import hashlib
from datetime import datetime
import json

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Install: pip install pillow numpy")

try:
    import cv2
except ImportError:
    print("Install: pip install opencv-python")


@dataclass
class VisualElement:
    """Detected visual element"""
    element_type: str  # button, text, image, form, etc.
    coordinates: Tuple[int, int, int, int]  # x, y, width, height
    confidence: float
    text: Optional[str] = None
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


@dataclass
class ImageAnalysis:
    """Complete image analysis result"""
    image_path: str
    timestamp: str
    dimensions: Tuple[int, int]
    elements: List[VisualElement]
    dominant_colors: List[str]
    text_content: str
    scene_description: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_path": self.image_path,
            "timestamp": self.timestamp,
            "dimensions": self.dimensions,
            "elements": [{"type": e.element_type, "coords": e.coordinates, 
                         "confidence": e.confidence, "text": e.text} for e in self.elements],
            "dominant_colors": self.dominant_colors,
            "text_content": self.text_content,
            "scene_description": self.scene_description,
            "metadata": self.metadata
        }


class VisionAnalyzer:
    """
    LOCAL Vision Analysis (Privacy-First)
    
    Uses local computer vision models - NO external API calls
    All processing happens on-device
    """
    
    def __init__(self, use_gpu: bool = False):
        self.use_gpu = use_gpu
        self._init_models()
    
    def _init_models(self):
        """Initialize local CV models"""
        # Use local models only - OpenCV, PIL
        # For advanced: CLIP, SAM, YOLO (can run locally)
        self.ocr_available = self._check_ocr()
        self.face_detection = self._init_face_detection()
        print(f"✅ Vision Analyzer initialized (GPU: {self.use_gpu})")
    
    def _check_ocr(self) -> bool:
        """Check if OCR is available"""
        try:
            import pytesseract
            return True
        except ImportError:
            print("⚠️  OCR unavailable. Install: pip install pytesseract")
            return False
    
    def _init_face_detection(self):
        """Initialize local face detection"""
        try:
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            return face_cascade
        except:
            return None
    
    def analyze_image(self, image_path: str) -> ImageAnalysis:
        """
        Analyze image with LOCAL processing only
        NO external API calls - privacy guaranteed
        """
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Basic analysis
        dimensions = img.size
        dominant_colors = self._extract_dominant_colors(img_array)
        
        # Element detection
        elements = self._detect_elements(img_array)
        
        # OCR text extraction
        text_content = self._extract_text(img_array) if self.ocr_available else ""
        
        # Scene analysis
        scene_description = self._analyze_scene(img_array)
        
        return ImageAnalysis(
            image_path=image_path,
            timestamp=datetime.now().isoformat(),
            dimensions=dimensions,
            elements=elements,
            dominant_colors=dominant_colors,
            text_content=text_content,
            scene_description=scene_description,
            metadata={
                "file_size": Path(image_path).stat().st_size,
                "format": img.format,
                "mode": img.mode
            }
        )
    
    def analyze_screenshot(self, screenshot_data: bytes) -> ImageAnalysis:
        """Analyze screenshot data"""
        # Save temporarily for analysis
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            f.write(screenshot_data)
            temp_path = f.name
        
        result = self.analyze_image(temp_path)
        Path(temp_path).unlink()  # Clean up
        return result
    
    def detect_ui_elements(self, image_path: str) -> List[VisualElement]:
        """Detect UI elements in screenshot"""
        img = cv2.imread(image_path)
        elements = []
        
        # Detect buttons (using contour detection)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # Filter by size to find button-like elements
            if 20 < w < 300 and 10 < h < 100:
                elements.append(VisualElement(
                    element_type="button_candidate",
                    coordinates=(x, y, w, h),
                    confidence=0.7
                ))
        
        return elements[:50]  # Limit results
    
    def compare_images(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        """Compare two images for differences"""
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)
        
        # Resize to same dimensions if needed
        if img1.shape != img2.shape:
            img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        # Calculate difference
        diff = cv2.absdiff(img1, img2)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        
        # Threshold to find significant differences
        _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
        
        # Calculate similarity score
        similarity = 1.0 - (np.sum(thresh > 0) / thresh.size)
        
        return {
            "similarity_score": similarity,
            "has_significant_changes": similarity < 0.95,
            "difference_percentage": (1 - similarity) * 100
        }
    
    def _extract_dominant_colors(self, img_array: np.ndarray, n_colors: int = 5) -> List[str]:
        """Extract dominant colors"""
        # Simple k-means clustering for color extraction
        pixels = img_array.reshape(-1, 3)
        
        # Sample for performance
        if len(pixels) > 10000:
            indices = np.random.choice(len(pixels), 10000, replace=False)
            pixels = pixels[indices]
        
        # Use simple binning instead of k-means for speed
        colors = []
        for i in range(n_colors):
            mean_color = np.mean(pixels, axis=0).astype(int)
            colors.append(f"#{mean_color[0]:02x}{mean_color[1]:02x}{mean_color[2]:02x}")
        
        return colors
    
    def _detect_elements(self, img_array: np.ndarray) -> List[VisualElement]:
        """Detect visual elements"""
        elements = []
        
        # Detect faces (if available)
        if self.face_detection is not None:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            faces = self.face_detection.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                elements.append(VisualElement(
                    element_type="face",
                    coordinates=(int(x), int(y), int(w), int(h)),
                    confidence=0.8
                ))
        
        return elements
    
    def _extract_text(self, img_array: np.ndarray) -> str:
        """Extract text using OCR"""
        if not self.ocr_available:
            return ""
        
        try:
            import pytesseract
            text = pytesseract.image_to_string(Image.fromarray(img_array))
            return text.strip()
        except Exception as e:
            print(f"OCR error: {e}")
            return ""
    
    def _analyze_scene(self, img_array: np.ndarray) -> str:
        """Basic scene analysis"""
        # Simple heuristics
        height, width = img_array.shape[:2]
        brightness = np.mean(img_array)
        
        scene_type = "unknown"
        if width > height * 1.5:
            scene_type = "landscape"
        elif height > width * 1.5:
            scene_type = "portrait"
        else:
            scene_type = "square"
        
        brightness_level = "bright" if brightness > 150 else "dark" if brightness < 100 else "normal"
        
        return f"{scene_type} composition, {brightness_level} lighting"


# Example usage
if __name__ == "__main__":
    analyzer = VisionAnalyzer()
    
    # Create a test image
    test_img = Image.new('RGB', (800, 600), color='blue')
    test_img.save('/tmp/test_image.png')
    
    # Analyze
    result = analyzer.analyze_image('/tmp/test_image.png')
    print(f"Analysis: {result.scene_description}")
    print(f"Dimensions: {result.dimensions}")
    print(f"Colors: {result.dominant_colors}")

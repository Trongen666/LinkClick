// import { useState, useRef, useCallback, useEffect } from 'react';
// import Webcam from 'react-webcam';
// import { motion } from 'framer-motion';
// import * as faceapi from 'face-api.js';

// const FaceLoginComponent = ({ username, onCapture, onCancelCapture, onSwitchToOTP }) => {
//   const webcamRef = useRef(null);
//   const [isLoading, setIsLoading] = useState(true);
//   const [faceDetected, setFaceDetected] = useState(false);
//   const [modelsLoaded, setModelsLoaded] = useState(false);
//   const [errorMsg, setErrorMsg] = useState('');
  
//   // Configure webcam
//   const videoConstraints = {
//     width: 300,
//     height: 300,
//     facingMode: "user"
//   };
  
//   // Load face-api models
//   useEffect(() => {
//     const loadModels = async () => {
//       try {
//         await Promise.all([
//           faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
//           faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
//           faceapi.nets.faceRecognitionNet.loadFromUri('/models')
//         ]);
//         setModelsLoaded(true);
//       } catch (error) {
//         console.error('Error loading face detection models:', error);
//         setErrorMsg('Could not load face detection models');
//       }
//       setIsLoading(false);
//     };
    
//     loadModels();
    
//     // Create models directory if it doesn't exist in public folder
//     // Note: In production, you need to ensure these models are available
    
//     return () => {
//       // Cleanup
//     };
//   }, []);
  
//   // Detect faces periodically
//   useEffect(() => {
//     let interval;
    
//     if (webcamRef.current && webcamRef.current.video && modelsLoaded) {
//       interval = setInterval(async () => {
//         if (webcamRef.current && webcamRef.current.video.readyState === 4) {
//           try {
//             const detections = await faceapi.detectAllFaces(
//               webcamRef.current.video,
//               new faceapi.TinyFaceDetectorOptions()
//             );
            
//             setFaceDetected(detections.length > 0);
//           } catch (error) {
//             console.error('Face detection error:', error);
//           }
//         }
//       }, 500);
//     }
    
//     return () => {
//       if (interval) clearInterval(interval);
//     };
//   }, [modelsLoaded]);
  
//   // Capture function
//   const capture = useCallback(() => {
//     if (!webcamRef.current) return;
    
//     const imageSrc = webcamRef.current.getScreenshot();
//     if (!imageSrc) {
//       setErrorMsg('Failed to capture image');
//       return;
//     }
    
//     // Convert base64 to blob
//     const base64Data = imageSrc.replace(/^data:image\/jpeg;base64,/, '');
//     const byteCharacters = atob(base64Data);
//     const byteNumbers = new Array(byteCharacters.length);
    
//     for (let i = 0; i < byteCharacters.length; i++) {
//       byteNumbers[i] = byteCharacters.charCodeAt(i);
//     }
    
//     const byteArray = new Uint8Array(byteNumbers);
//     const blob = new Blob([byteArray], { type: 'image/jpeg' });
    
//     // Send to parent component
//     onCapture(blob);
//   }, [onCapture]);
  
//   if (isLoading) {
//     return (
//       <div className="flex flex-col items-center justify-center p-6">
//         <div className="w-64 h-64 rounded-lg glass-panel flex items-center justify-center">
//           <div className="text-highlight animate-pulse">Loading camera...</div>
//         </div>
//       </div>
//     );
//   }
  
//   return (
//     <motion.div 
//       className="flex flex-col items-center p-4"
//       initial={{ opacity: 0 }}
//       animate={{ opacity: 1 }}
//       transition={{ duration: 0.5 }}
//     >
//       <div className="mb-4 text-center">
//         <h3 className="text-lg text-white">Face Login</h3>
//         <p className="text-sm text-gray-300">Position your face in the frame</p>
//       </div>
      
//       <div className={`
//         relative w-72 h-72 rounded-lg overflow-hidden
//         ${faceDetected ? 'border-2 border-highlight glow-effect' : 'border-2 border-gray-600'}
//       `}>
//         <Webcam
//           audio={false}
//           ref={webcamRef}
//           screenshotFormat="image/jpeg"
//           videoConstraints={videoConstraints}
//           className="w-full h-full object-cover"
//           onUserMediaError={(error) => {
//             console.error('Webcam error:', error);
//             setErrorMsg('Could not access camera. Please check permissions.');
//           }}
//         />
        
//         {/* Face detection indicator */}
//         {faceDetected && (
//           <div className="absolute bottom-2 left-2 bg-green-500 px-2 py-1 rounded-md text-xs">
//             Face Detected
//           </div>
//         )}
//       </div>
      
//       {errorMsg && (
//         <div className="mt-2 text-red-500 text-sm">{errorMsg}</div>
//       )}
      
//       <div className="mt-6 flex flex-col space-y-3 w-full">
//         <button
//           onClick={capture}
//           disabled={!faceDetected}
//           className={`
//             w-full py-2 px-4 rounded-lg font-medium text-white
//             ${faceDetected 
//               ? 'bg-gradient-to-r from-primary-600 to-highlight hover:opacity-90' 
//               : 'bg-gray-700 cursor-not-allowed'}
//             transition duration-300 ease-in-out transform hover:scale-[1.02]
//           `}
//         >
//           Authenticate with Face
//         </button>
        
//         <button
//           onClick={onSwitchToOTP}
//           className="text-sm text-accent hover:text-highlight transition-colors duration-300"
//         >
//           Use OTP Instead
//         </button>
        
//         <button
//           onClick={onCancelCapture}
//           className="text-sm text-gray-400 hover:text-white transition-colors duration-300"
//         >
//           Back to Username
//         </button>
//       </div>
//     </motion.div>
//   );
// };

// export default FaceLoginComponent;

import React from 'react';
import { useFaceDetection } from 'react-use-face-detection';
import Webcam from 'react-webcam';
import { motion } from 'framer-motion';

const FaceLoginComponent = ({ username, onCapture, onCancelCapture, onSwitchToOTP }) => {
  const {
    webcamRef,
    boundingBox,
    isLoading,
    detected,
    facesDetected,
  } = useFaceDetection({
    faceDetectionOptions: { model: 'short' },
    mirrored: true,
  });

  const capture = async () => {
    const screenshot = webcamRef.current?.getScreenshot();
    if (!screenshot) return;

    try {
      const response = await fetch(screenshot);
      const blob = await response.blob();
      onCapture(blob);
    } catch (error) {
      console.error("Image capture failed", error);
    }
  };

  return (
    <motion.div 
      className="flex flex-col items-center p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mb-4 text-center">
        <h3 className="text-lg text-white">Face Login</h3>
        <p className="text-sm text-gray-300">Position your face in the frame</p>
      </div>

      <div className={`
        relative w-72 h-72 rounded-lg overflow-hidden
        ${detected ? 'border-2 border-highlight glow-effect' : 'border-2 border-gray-600'}
      `}>
        <Webcam
          ref={webcamRef}
          audio={false}
          mirrored={true}
          screenshotFormat="image/jpeg"
          videoConstraints={{
            width: 300,
            height: 300,
            facingMode: 'user'
          }}
          className="w-full h-full object-cover"
          onUserMediaError={(err) => {
            console.error("Webcam access error:", err);
          }}
        />

        {detected && (
          <div className="absolute bottom-2 left-2 bg-green-500 px-2 py-1 rounded-md text-xs">
            Face Detected ({facesDetected})
          </div>
        )}
      </div>

      <div className="mt-6 flex flex-col space-y-3 w-full">
        <button
          onClick={capture}
          disabled={!detected}
          className={`
            w-full py-2 px-4 rounded-lg font-medium text-white
            ${detected 
              ? 'bg-gradient-to-r from-primary-600 to-highlight hover:opacity-90' 
              : 'bg-gray-700 cursor-not-allowed'}
            transition duration-300 ease-in-out transform hover:scale-[1.02]
          `}
        >
          Authenticate with Face
        </button>

        <button
          onClick={onSwitchToOTP}
          className="text-sm text-accent hover:text-highlight transition-colors duration-300"
        >
          Use OTP Instead
        </button>

        <button
          onClick={onCancelCapture}
          className="text-sm text-gray-400 hover:text-white transition-colors duration-300"
        >
          Back to Username
        </button>
      </div>
    </motion.div>
  );
};

export default FaceLoginComponent;

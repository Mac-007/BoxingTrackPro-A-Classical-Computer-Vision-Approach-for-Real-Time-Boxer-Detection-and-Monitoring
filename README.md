# BoxingTrackPro: A Classical Computer Vision Approach for Real-Time Boxer Detection and Monitoring

### Overview
**BoxingTrackPro** is a classical computer vision model designed to detect and monitor boxers in real-time using classical image processing algorithms. The project focuses on distinguishing boxers based on their outfit colors—red for one player and blue for the other—according to standard boxing match regulations.

This project aims to provide an efficient and accurate method to track boxers' positions and movements throughout a match, generating an output video and a NumPy file with the tracked data.

### Features
- **Real-Time Boxer Detection**: Identifies and tracks boxers in a video stream using color-based detection.
- **Classical Image Processing Algorithms**: Utilizes image processing techniques like HSV color thresholding, morphological operations, and contour detection.
- **Output Generation**: Produces an annotated video and a NumPy file containing the tracked positions and movements of the boxers.


### Workflow
![2_Pipeline](https://github.com/user-attachments/assets/e287442a-8056-42e1-9762-2d7620e61228)
1. **Video Capture and Initialization**: Read the input video file and initialize necessary parameters.
2. **HSV Color Thresholding (Blue & Red)**: Convert the video frames to HSV color space and apply color thresholds to isolate the blue and red regions corresponding to the boxers.
3. **Morphological Operations (Erosion and Dilation)**: Perform morphological operations to clean up noise and improve the detection accuracy.
4. **Contour Detection and Analysis**: Detect contours in the thresholded frames and analyze them to identify potential boxer regions.
5. **Region of Interest (ROI) Validation**: Validate the detected regions to ensure they correspond to the expected boxer positions.
6. **Bounding Box Calculation and Update**: Calculate and update the bounding boxes around the detected boxers.
7. **Centroid Computation**: Compute the centroids of the bounding boxes to track the movement of the boxers.
8. **Frame Display**: Display the processed frames with annotated bounding boxes and centroids.
9. **Positional Data Storage**: Store the positional data of the boxers in a NumPy file for further analysis.
10. **Output Video Generation**: Generate an output video with the tracked positions and movements of the boxers.

### Output
![Picture3](https://github.com/user-attachments/assets/5f856dab-4aeb-4451-ab5b-96c84a5372d7)

### Installation
To use BoxingTrackPro, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/BoxingTrackPro.git
   cd BoxingTrackPro
   ```

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.



### Contact
For any questions or inquiries, please contact amitchougule121@gmail.com.

---

Thank you for using BoxingTrackPro! We hope this project helps you in your computer vision endeavors. Happy coding!

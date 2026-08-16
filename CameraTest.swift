import AVFoundation

final class CameraTest: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate {

    private let session = AVCaptureSession()

    func start() {
        // Request permission
        AVCaptureDevice.requestAccess(for: .video) { [weak self] granted in
            guard granted else {
                print("❌ Camera permission denied")
                return
            }

            print("✅ Camera permission granted")
            self?.setupCamera()
        }
    }

    private func setupCamera() {
        session.beginConfiguration()
        session.sessionPreset = .high

        // Find rear camera
        guard let camera = AVCaptureDevice.default(
            .builtInWideAngleCamera,
            for: .video,
            position: .back
        ) else {
            print("❌ No camera found")
            return
        }

        print("✅ Camera found: \(camera.localizedName)")

        // Create camera input
        do {
            let input = try AVCaptureDeviceInput(device: camera)

            guard session.canAddInput(input) else {
                print("❌ Cannot add camera input")
                return
            }

            session.addInput(input)
            print("✅ Camera input added")
        } catch {
            print("❌ Failed to create camera input: \(error)")
            return
        }

        // Create video output
        let output = AVCaptureVideoDataOutput()

        let queue = DispatchQueue(
            label: "camera.capture.queue"
        )

        output.setSampleBufferDelegate(self, queue: queue)

        guard session.canAddOutput(output) else {
            print("❌ Cannot add video output")
            return
        }

        session.addOutput(output)

        print("✅ Video output added")

        session.commitConfiguration()

        // Start capture
        session.startRunning()

        print("📷 Camera session started")
    }

    // Called every time a frame arrives
    func captureOutput(
        _ output: AVCaptureOutput,
        didOutput sampleBuffer: CMSampleBuffer,
        from connection: AVCaptureConnection
    ) {
        guard let imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else {
            return
        }

        let width = CVPixelBufferGetWidth(imageBuffer)
        let height = CVPixelBufferGetHeight(imageBuffer)

        print("📸 Frame received: \(width)x\(height)")
    }
}
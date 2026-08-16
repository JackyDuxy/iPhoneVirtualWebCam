import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Camera Test")
            .onAppear {
                CameraTest().start()
            }
    }
}
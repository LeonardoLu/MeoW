//
//  ContentView.swift
//  SpineSpriteOnWatch Watch App
//
//  Created by lujunhui.2nd on 2023/1/1.
//

import SwiftUI
import SpriteKit
import UIKit

struct ContentView: View {
    var body: some View {
        GeometryReader { proxy in
            SpriteView(scene: GameScene(size: proxy.size))
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

//
//  WatchSKView.swift
//  SpineSpriteOnWatch Watch App
//
//  Created by lujunhui.2nd on 2023/1/1.
//


import SwiftUI
import SpriteKit
//
//class GameView: SKView, UIViewRepresentable {
//
//    // Conformance to UIViewRepresentable
//    func makeUIView(context: Context) -> SKView {
//        print("Make UIView")
//        return GameView(frame: UIScreen.main.bounds)
//    }
//    func updateUIView(_ uiView: SKView, context: Context) {
//        print("Update UIView")
//    }
//
//    // Creating scene
//    override init(frame: CGRect) {
//        super.init(frame: frame)
//
//        let scene = GameScene(size: UIScreen.main.bounds.size)
//        scene.scaleMode = .aspectFill
//        presentScene(scene)
//        self.presentScene(scene)
//
//        self.ignoresSiblingOrder = true
//
//        //debug info
//        self.showsFPS = true
//        self.showsNodeCount = true
//        self.showsDrawCount = true
//    }
//    required init?(coder: NSCoder) {
//        fatalError("init(coder:) has not been implemented")
//    }
//}
class GameScene: SKScene {
    override func sceneDidLoad() {
        do {

            let character = try Skeleton(json: "windmill-ess", folder: "windmill-ess", skin: nil)
            character.name = "character"
            character.position = CGPoint(x: self.size.width / 2, y: (self.size.height / 2)-20)
            addChild(character)
            character.setScale(0.15)

            let animation = try character.action(animation: "animation")
            character.run(.repeatForever(animation))
//
//            let walkAnimation = try character.action(animation: "walk")
//            character.run(.repeatForever(walkAnimation))
//
//            let switchSkinsAction = SKAction.sequence([.wait(forDuration: 3),
//                                                       try character.action(applySkin: "goblingirl"),
//                                                       .wait(forDuration: 3),
//                                                       try character.action(applySkin: "goblin")])
//
//            character.run(.repeatForever(switchSkinsAction))

        } catch {

            print(error)
        }
    }
}

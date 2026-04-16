import UIKit
import WebKit

class ViewController: UIViewController, WKNavigationDelegate {

    var webView: WKWebView!

    override func viewDidLoad() {
        super.viewDidLoad()

        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true

        webView = WKWebView(frame: view.bounds, configuration: config)
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        webView.navigationDelegate = self
        webView.allowsBackForwardNavigationGestures = true
        view.addSubview(webView)

        if let url = URL(string: "https://wine-pairing.online") {
            webView.load(URLRequest(url: url))
        }
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        print("Page loaded successfully")
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("Navigation failed: \(error.localizedDescription)")
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        print("Provisional navigation failed: \(error.localizedDescription)")
    }

    override var prefersStatusBarHidden: Bool {
        return false
    }
}

cask "pickhex" do
  version "1.1.1"
  sha256 :no_check

  url "https://github.com/murrer33/PickHex/releases/download/v#{version}/PickHex-macOS.zip"
  name "PickHex"
  desc "Lightweight Menu Bar color picker and eyedropper with HEX, RGB, HSL & Tailwind support"
  homepage "https://github.com/murrer33/PickHex"

  app "PickHex.app"

  postflight do
    system_command "/usr/bin/xattr",
                   args: ["-cr", "#{appdir}/PickHex.app"],
                   sudo: false
  end

  zap trash: [
    "~/.pickhex",
    "~/Library/LaunchAgents/com.pickhex.eyedropper.plist",
  ]
end

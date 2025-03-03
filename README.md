# TextFX

TextFX is a powerful API for creating stylized text effects, perfect for Discord and other messaging platforms. Transform plain text into eye-catching animated and static effects.

## 🌟 Features

- **Gradient Text**: Static and animated RGB gradient effects
- **Neon Glow**: Text with vibrant neon glow effects
- **Rainbow Wave**: Dynamic rainbow pattern text
- **Glitch Effect**: Animated glitch/corruption effects
- Transparent backgrounds for seamless integration
- Easy-to-use REST API
- CORS enabled for web applications

## 🚀 API Endpoints

Base URL: `http://your-domain.com/api/v1`

### Static Effects

#### Gradient Text
```
GET /gradient-text?text=Your%20Text
```
Returns a PNG image with a static RGB gradient effect.

#### Neon Text
```
GET /neon?text=Your%20Text
```
Returns a PNG image with a neon glow effect.

#### Rainbow Wave
```
GET /rainbow-wave?text=Your%20Text
```
Returns a PNG image with a rainbow wave pattern.

### Animated Effects

#### Animated Gradient
```
GET /gradient-text.gif?text=Your%20Text
```
Returns an animated GIF with a scrolling RGB gradient effect.

#### Glitch Effect
```
GET /glitch.gif?text=Your%20Text
```
Returns an animated GIF with a glitch/corruption effect.

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Bentlybro/TextFX.git
cd TextFX
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```
The server will start on port 1754 by default.

## 💻 Development

### Requirements
- Python 3.7+
- PIL (Pillow)
- Flask
- NumPy
- Flask-CORS

### Project Structure
```
TextFX/
├── app.py              # Main Flask application
├── generators/         # Text effect generators
│   ├── gradient_text.py
│   ├── neon_text.py
│   ├── rainbow_wave.py
│   ├── glitch_text.py
│   └── utils.py
└── requirements.txt    # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new text effects
- Improve existing effects
- Fix bugs
- Enhance documentation

Please submit a pull request with your changes.

## 📝 License

MIT License - feel free to use this in your own projects!

## 🔗 Links

- [GitHub Repository](https://github.com/Bentlybro/TextFX)
- [Issue Tracker](https://github.com/Bentlybro/TextFX/issues)

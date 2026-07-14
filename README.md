#  HADI Object Detector

YOLOv8 aur Streamlit se bana hua ek Object Detection web app. Ye app kisi bhi
image mein real-world objects (log, cars, animals, etc.) ko detect karke
un par boxes bana deta hai.

---

##  Project Structure

```
HADI-Object-Detector/
│
├── app.py                 # Main Streamlit app (UI yahan hai)
├── detector.py             # YOLOv8 model load aur detection logic
├── requirements.txt        # Zaroori Python libraries ki list
├── README.md                # Ye guide file
├── .gitignore               # GitHub par kya upload nahi karna
│
├── models/
│   └── yolov8n.pt            # YOLOv8 Nano model file
│
└── utils/
    ├── __init__.py            # Isse "utils" ek package ban jata hai
    ├── image_info.py           # Image ki details nikalne wala code
    └── summary.py               # Detection summary banane wala code
```

**Important:** `models/` aur `utils/` dono folders `app.py` ke barabar
(sath waali level) mein hone chahiye, andar nahi.

---

## 🖥️ Step 1 — VS Code mein Folder Set Karna

1. Apne computer par ek folder banayein, naam do: `HADI-Object-Detector`
2. VS Code kholein → `File` → `Open Folder` → wahi folder select karein.
3. Is folder ke andar do sub-folders banayein:
   - `models`
   - `utils`

   (VS Code ke left side "Explorer" panel mein right-click karke
   "New Folder" se ban jate hain)

4. Saari files jo maine di hain, unko sahi jagah rakhein:
   `app.py`, `detector.py`, `requirements.txt`, `README.md`, `.gitignore`
    → **root folder** mein (sabse bahar)
    `yolov8n.pt` → **models/** folder ke andar
    `__init__.py`, `image_info.py`, `summary.py` → **utils/** folder ke andar

---

##  Step 2 — Python Environment Set Karna

VS Code ka **Terminal** kholein (`Ctrl + ~` ya `` Terminal → New Terminal ``)
aur ye commands ek ek karke chalayein:

### a) Virtual environment banayein (recommended — isse aapke computer
ka Python clean rehta hai)

```bash
python -m venv venv
```

### b) Activate karein

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

Activate hone ke baad terminal ke shuru mein `(venv)` likha dikhega.

### c) Zaroori libraries install karein

```bash
pip install -r requirements.txt
```

Isme thora time lagega (ultralytics aur opencv download hongi), sabar karein ☕

---

## ▶️ Step 3 — App Run Karna

```bash
streamlit run app.py
```

Chalane ke baad automatically browser mein ek tab khulega
(`http://localhost:8501`). Agar na khule to terminal mein diya gaya link
copy karke browser mein paste kar dein.

---

## Kya Naya / Behtar Kiya Gaya Hai (Changes Summary)

| Pehle | Ab |
|---|---|
| `utils.image_info` aur `utils.summary` files missing thin — app crash hota tha | Dono files ban chuki hain aur kaam kar rahi hain |
| Result image ke colors ulte (BGR) aate the | RGB mein fix kar diya gaya hai |
| Model path hardcoded/uncertain | Model path automatically project folder se detect hota hai |
| Koi error handling nahi thi | Ab agar model na mile ya galat file upload ho to sahi message dikhta hai |
| Confidence fixed thi | Sidebar mein slider se confidence adjust kar sakte hain |
| Result download nahi ho sakta tha | Ab "Download Result Image" button hai |
| Basic UI | Icons, spinner (loading animation), aur cleaner layout add kiya |

---

## 🚀 Step 4 — Internet Par Free Deploy Karna (Optional, "Top" Impression ke Liye)

Internship ke liye agar aap ye app live link ke sath submit karna chahte
hain (sirf code nahi), to ye karein:

1. GitHub par account banayein (agar nahi hai): https://github.com
2. Is poore folder ko GitHub par ek naye repository mein upload karein
   (VS Code ke left side "Source Control" icon se bhi ho sakta hai, ya
   GitHub Desktop app use kar sakte hain).
3. https://share.streamlit.io par jayein → GitHub se login karein →
   apni repository select karein → `app.py` ko main file batayein → Deploy.
4. Kuch minute mein aapko ek live public link mil jayega jo kisi ke sath
   bhi share kar sakte hain (koi installation ki zaroorat nahi hogi unhe).

Ye cheez internship report mein bohat acha impression deti hai kyunke
sirf code nahi, ek **live working product** dikhata hai.

---

## 🛠️ Common Problems (Agar Error Aaye)

- **`ModuleNotFoundError`** → `pip install -r requirements.txt` dobara chalayein,
  aur check karein `(venv)` activate hai ya nahi.
- **Model file not found** → check karein `yolov8n.pt` `models/` folder ke
  andar hi hai, kahin aur nahi.
- **App bohat slow hai** → pehli dafa model load hone mein thora time lagta
  hai, uske baad fast ho jata hai (cache ki wajah se).

---

##  Aage Kya Improve Kar Sakte Hain (Future Ideas)

- Webcam / live video se real-time detection
- Multiple images ek sath upload karke batch detection
- Bigger YOLOv8 model (yolov8s/m) use karke accuracy improve karna
- Detected objects ko category ke hisaab se filter karna (sirf "person" dikhao, etc.)

---

Made with  using YOLOv8 + Streamlit.

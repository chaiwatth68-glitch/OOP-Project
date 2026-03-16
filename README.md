# ✨ Premium Memory Game

สะกดรอยตามเสียงและแสงสว่าง! เกม **Memory Game** แบบคลาสสิกที่ถูกพัฒนาขึ้นใหม่ด้วย **Python** และ **Pygame** ในรูปแบบพรีเมียม ตอบสนองเร็วทันใจ (Fast Responsive) และจัดระเบียบโค้ดตามสถาปัตยกรรม OOP และ SOLID Principles

---

## 🎯 จุดประสงค์ของโครงการ (Project Purpose)
- **เพื่อฝึกฝนและแสดงทักษะการเขียนโปรแกรมเชิงวัตถุ (OOP)** และหลักการ **SOLID Principles** (โดยเฉพาะ SRP - Single Responsibility Principle) ในโปรเจกต์งานเกม
- **สร้างสรรค์ User Experience (UX) ที่ดี** ให้กับเกมหน้าต่าง 2D พรีเมียม ด้วยความลื่นไหล ตอบสนองไว และดูทันสมัย

## 👥 กลุ่มเป้าหมาย (Target Audience)
- **ผู้เล่นทั่วไป (Casual Gamers)**: ที่ชื่นชอบเกมแนวฝึกทักษะสมอง เสริมสร้างความจำ (Brain Trainer)
- **นักเรียน / นักพัฒนา (Developers)**: ผู้ที่กำลังศึกษาการพัฒนาเกมด้วย Pygame หรือต้องการเรียนรู้โครงสร้าง Clean Code ที่แยกสัดส่วนชัดเจน

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)
* **ภาษาพัฒนา**: `Python 3.10+`
* **ไลบรารีขับเคลื่อนหลัก**: `Pygame 2.6.1` (เหมาะสำหรับเรนเดอร์ 2D Fast Layout และ Handler Sound Beep)
* **การจัดการแพ็กเกจ (Package Managers)**: 
  * `uv` (แนะนำสำหรับการพัฒนาซิงค์ฟลูรันได้ไว)
  * `Standard pip` (พื้นฐานทั่วไปที่ทุกคนเปิดใช้งานได้)

---

## 🎮 ฟีเจอร์เด่น (Key Features)

*   **Premium Aesthetics**: อินเตอร์เฟซหรูหราพร้อมกล่องเงา (Drop Shadow) และเอฟเฟกต์กระพริบที่เนียนตาทั้งหน้า Menu และ Game
*   **Multi-Difficulty Grids**: ท้าทายได้ 3 ระดับความยาก (Easy, Medium, Hard) โดยตารางจะขยายขนาดตามจำนวนสีที่ต้องจำ (2x2, 2x3 และ 3x3)
*   **Fast-Stream Input**: ไม่ต้องรอคิวแฟลชจบ! สามารถกดแท็บคอสตามสเตจ AI ได้ไวทวีคูณ (ตอบสนองเร็ว)
*   **Sound Feedback System**: ระบบเสียง Sound Beep แตกต่างโทน ทำให้ใช้งานได้แม้มองภาพไม่ทัน
*   **OOP/SOLID Architecture**: ออกแบบสถาปัตยกรรมแยก `View` (Rendering) และ `Logic` ขาดจากกัน ปรับปรุงโค้ดง่าย

---

## 🛠️ วิธีการติดตั้งและรันเกม (Installation & Setup)

ทำตามขั้นตอนด้านล่างนี้ และคุณจะสามารถเปิดเกมเล่นได้ทันทีภายใน 1 นาที!

### 🔹 วิธีที่ 1: ติดตั้งผ่าน Pip มาตรฐาน (Standard Setup)
เหมาะสำหรับผู้ใช้ทั่วไปที่มี Python 3.10 ขึ้นไปอยู่แล้ว:

1. **สร้างและเปิดระบบ Virtual Environment (แนะนำเพื่อความสะอาดยูสเซอร์)**:
   * **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **Mac / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
2. **ติดตั้ง Libraries จาก Requirements ที่ตรงระบบ**:
   ```bash
   pip install -r requirements.txt
   ```
3. **รันเกมหลัก**:
   ```bash
   python main.py
   ```

---

### 🔹 วิธีที่ 2: ติดตั้งผ่าน `uv` (Modern & Super Fast)
หากคุณใช้งานเครื่องมือจัดการระดับโมเดิร์น `uv` สามารถรันแบบสะอาดและตรง Lock file ได้เลย:

1. **ซิงค์สภาพแวดล้อม (Sync Virtual Environment)**:
   ```bash
   uv sync
   ```
2. **รันแอปพลิเคชัน**:
   ```bash
   uv run main.py
   ```

---

## 📂 โครงสร้างไฟล์ (File Structure)

*   `main.py` - จุดรันโปรแกรม และ Event Loop ภาพรวม
*   `game.py` - สมองของเกม Simon Says โลจิก Matching Sequence ขั้นสูง
*   `game_view.py` - จัดการด้านกราฟิก หน้าต่าง และ Popup ชัยชนะ
*   `menu.py` & `menu_view.py` - คอนโทรลหน้าจอเปลี่ยนด่านเมนูหลัก
*   `button.py` - ขุมทรัพย์ปุ่มกดสีพร้อม Drop Shadow ไดนามิก
*   `constants.py` - เก็บตารางรวมค่าความหน่วง สี และ Layout มิติต่างๆ
*   `sound_manager.py` - คอนโทรลควบคุมเสียง Beep

---

## 🕹️ วิธีการเล่น (How to Play)

1. เข้าหน้าเมนู เลือกความยาก **Easy, Medium, หรือ Hard**
2. รอดูจังหวะแฟลชสีและเสียง Sound Wave จากฝั่ง AI สั่งการ
3. จำลำดับสี และ **กดคลิกหน้าปุ่มให้ตรงตามลำดับ** ที่ขึ้นก่อนหน้า
4. ปั๊ม Stage ไปเรื่อยๆ จนจบด่าน ปักสแตนเก็บ High Score ให้ได้สูงสุด!
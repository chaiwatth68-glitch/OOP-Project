# ✨ Premium Simon Says

สะกดรอยตามเสียงและแสงสว่าง! เกม **Simon Says** แบบคลาสสิกที่ถูกพัฒนาขึ้นใหม่ด้วย **Python** และ **Pygame** ในรูปแบบพรีเมียม ตอบสนองเร็วทันใจ (Fast Responsive) และจัดระเบียบโค้ดตามสถาปัตยกรรม OOP และ SOLID Principles 

---

## 🎮 ฟีเจอร์เด่น (Key Features)

*   **Premium Aesthetics**: อินเตอร์เฟซหรูหราพร้อม Drop Shadow และแสงสะท้อนเงาที่สวยงาม
*   **Multi-Difficulty Grids**: มีให้เลือกเล่น 3 ระดับความยาก (Easy, Medium, Hard) พร้อมตารางปิ๊บแบบ 2x2, 3x2 และ 4x2 คอลัมน์
*   **Fast-Stream Input**: สามารถกดตอบรับ (Match-along) ตามจังหวะที่ AI แสดงสีได้ทันที ไม่ต้องนั่งแช่นิ่งรอคิวค้าง
*   **Sound Feedback System**: รองรับผลลัพธ์จากเสียง Beep แตกต่างกันระหว่างตา AI และตาผู้เล่น
*   **SOLID Architecture**: โครงสร้างแยกส่วน Game Logic กับ Rendering ออกจากกันอย่างชัดเจนตามมาตรฐาน SRP

---

## 🛠️ วิธีการติดตั้งและรันเกม (Installation & Run)

### 1. ความต้องการของระบบ (Prerequisites)
*   **Python 3.10 ขึ้นไป** (ตรวจสอบโดยรัน `python --version`)
*   **Pip** หรือเครื่องมือจัดการอย่าง **uv** (ดูได้จาก `pyproject.toml` ในโปรเจกต์)

---

### 2. ขั้นตอนการติดตั้ง (Setup)

#### 🔹 แบบที่ 1: ติดตั้งผ่าน Pip ทั่วไป (Standard Setup)
1. ติดตั้งไลบรารี **Pygame**:
   ```bash
   pip install pygame
   ```
2. รันเกมทันที:
   ```bash
   python main.py
   ```

---

#### 🔹 แบบที่ 2: ติดตั้งผ่าน `uv` (Modern & Fast)
หากโปรเจกต์ของคุณใช้งาน `uv.lock` สามารถใช้คำสั่งนี้เพื่อความรวดเร็วและสะอาดของ Venv:
1. ซิงค์ตรรกะระบบ:
   ```bash
   uv sync
   ```
2. รันแอปพลิเคชัน:
   ```bash
   uv run main.py
   ```

---

## 📂 โครงสร้างไฟล์ (File Structure)

*   `main.py` - จุดเริ่มต้นของแอปและ Event Loop
*   `game.py` - ตรรกะของเกม Simon logic (Sequence และ checking)
*   `game_view.py` - โลจิก Rendering วาดหน้าแสดงผลและ Popup
*   `menu.py` และ `menu_view.py` - ดูแลระบบสลับคลาสเลือกความยาก
*   `button.py` - คลาสจัดการและอนิเมชั่น Drop-shadow ของปุ่มกดสี
*   `constants.py` - รวบรวมข้อมูลตั้งค่าระดับความเร็ว ความยาก หน้าจอและสี
*   `sound_manager.py` - ควบคุมเสียง Effect Beep

---

## 🕹️ วิธีการเล่น (How to Play)

1. เข้าหน้าเมนู เลือกความยาก **Easy, Medium, หรือ Hard**
2. รอดูจังหวะแฟลชสีและเสียงจาก AI สั่งการ
3. จำลำดับสี และ **กดคัดลอกตามสไตล์ AI** ให้ครบจบสเตจ
4. ปั๊ม Stage ไปเรื่อยๆ จนกว่าจะชนะขาด!
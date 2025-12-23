# 🏀 NBA Fantasy Dashboard: Troubleshooting & Setup Guide

This guide is designed for non-technical users to help resolve common issues when trying to get the dashboard live.

---

## 🚀 1. Quick Start (How to Run the App)

Instead of running multiple complex commands, I have created a **single launcher** for you.

**The Fix:**
1. Open your project folder.
2. Find the file named `start_app.bat`.
3. **Double-click it.**
4. Two new windows will open. **Do not close them.** 
   - One is the "Backend" (the brain).
   - One is the "Frontend" (the website you see).
5. Wait about 10 seconds, then open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔐 2. Database Error ("Table not found")

If you see a red box saying `Could not find the table 'public.league_settings'`, it means your private database isn't ready to store your information yet.

**The Fix:**
1. Login to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Click on your project.
3. On the left sidebar, click the **SQL Editor** icon (looks like `>_`).
4. Click **"+ New Query"**.
5. Paste the code below and click **Run**:

```sql
CREATE TABLE public.league_settings (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT,
  league_id TEXT NOT NULL,
  swid TEXT NOT NULL,
  espn_s2 TEXT NOT NULL,
  season INTEGER DEFAULT 2025,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
ALTER TABLE public.league_settings ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Manage own settings" ON public.league_settings FOR ALL USING (auth.uid() = id);
```

---

## 🔑 3. Finding Your ESPN Credentials

To see your private league data, the app needs three pieces of information from ESPN.

**The Fix:**
1. **League ID**: Open your ESPN league in your browser. Look at the address bar. The number after `leagueId=` is your ID.
2. **SWID & ESPN_S2**:
   - On your ESPN league page, press `F12` on your keyboard.
   - Click the **Application** tab at the top (it might be hidden under a `>>` symbol).
   - On the left, click **Cookies**, then `https://fantasy.espn.com`.
   - Look for `SWID` (copy the whole value including `{ }`).
   - Look for `espn_s2` (copy the very long string of letters and numbers).

---

## 🛠️ 4. Common Technical Issues We've Already Fixed

| Issue | What was happening? | Status |
| :--- | :--- | :--- |
| **Login Blinking** | The website was stuck in a loop because it couldn't remember you were logged in. | **FIXED** |
| **CORS Error** | The "Brain" (Backend) was refusing to talk to the "Face" (Frontend). | **FIXED** |
| **Basketball Icon Error** | A tiny typo in the code was crashing the Settings page. | **FIXED** |
| **Missing Uvicorn** | A necessary piece of software wasn't installed correctly. | **FIXED** |

---

## 💡 Troubleshooting Tips

- **Website looks broken?** Refresh the page using `Ctrl + F5` to clear the old "memory" of the site.
- **Can't log in?** Make sure the `start_app.bat` window is still open and doesn't show red text.
- **Still stuck?** If you see a new error, take a screenshot of the **entire screen** (including the address bar) and I will identify it immediately.

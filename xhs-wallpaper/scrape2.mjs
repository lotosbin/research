import fs from "node:fs/promises";

const task = await taskSpace("xhs wallpaper research");
const page = task.page("p1");
const OUT = "/Volumes/StorageMacMini/liubinbin/lotosbin/research/xhs-wallpaper/raw_xhs.json";

const keywords = [
  "%E6%89%8B%E6%9C%BA%E5%A3%81%E7%BA%B8",
  "%E5%A3%81%E7%BA%B8%20%E5%85%8D%E8%B4%B9",
  "iPhone%20%E5%A3%81%E7%BA%B8%20%E9%AB%98%E6%B8%85",
  "%E5%A3%81%E7%BA%B8%20%E5%AE%9A%E5%88%B6",
  "%E5%9B%BD%E9%A3%8E%20%E5%A3%81%E7%BA%B8"
];

const results = [];

for (const kw of keywords) {
  const url = "https://www.xiaohongshu.com/search_result?keyword=" + kw + "&type=51";
  try {
    await page.goto(url, { timeout: 30000 });
  } catch (e) {
    console.log("goto fail", kw, e.message);
    continue;
  }
  await page.waitForTimeout(2500);
  for (let i = 0; i < 2; i++) {
    await page.mouse.wheel(0, 1400);
    await page.waitForTimeout(800);
  }
  const cards = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll("section.note-item").forEach((el) => {
      const a = el.querySelector('a[href*="/search_result/"]');
      const t = el.querySelector(".title span")?.textContent?.trim();
      const au = el.querySelector(".author .name")?.textContent?.trim();
      const likes = el.querySelector(".like-wrapper .count")?.textContent?.trim();
      if (a && t && a.getAttribute("href").includes("xsec_token")) {
        out.push({ title: t, author: au, likes, href: a.getAttribute("href") });
      }
    });
    return out;
  });
  console.log("KW", kw, "cards", cards.length);
  for (const c of cards.slice(0, 6)) {
    let detail = null;
    try {
      await page.goto("https://www.xiaohongshu.com" + c.href, { timeout: 25000 });
      await page.waitForTimeout(2000);
      for (let i = 0; i < 4; i++) {
        await page.mouse.wheel(0, 1200);
        await page.waitForTimeout(600);
      }
      detail = await page.evaluate(() => {
        const txt = (sel) => document.querySelector(sel)?.textContent?.trim() || null;
        const comments = [...document.querySelectorAll(".comment-item")].map((c) => ({
          who: c.querySelector(".author .name")?.textContent?.trim() || null,
          text: c.querySelector(".content")?.textContent?.trim() || null,
          sub: c.querySelector(".date")?.textContent?.trim() || null
        })).filter((x) => x.text);
        return {
          title: txt("#detail-title"),
          desc: txt("#detail-desc"),
          likes: txt(".engage-bar-style .like-wrapper"),
          collects: txt(".engage-bar-style .collect-wrapper"),
          comments
        };
      });
    } catch (e) {
      detail = { error: e.message };
    }
    results.push({ keyword: kw, ...c, detail });
    console.log("  note", c.title, "comments:", detail && detail.comments ? detail.comments.length : (detail && detail.error ? detail.error.slice(0, 60) : 0));
  }
  await fs.writeFile(OUT, JSON.stringify(results, null, 1), "utf8");
}

console.log("SAVED", OUT, results.length);

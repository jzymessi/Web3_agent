import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# 创建保存路径
base_path = Path("aave_knowledge_base")
docs_path = base_path / "docs"
audits_path = base_path / "audits"
governance_path = base_path / "governance"

docs_path.mkdir(parents=True, exist_ok=True)
audits_path.mkdir(parents=True, exist_ok=True)
governance_path.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Part 1: 抓取 Aave 官方文档首页内容
# -----------------------------
def fetch_docs_homepage():
    url = "https://docs.aave.com/"
    response = requests.get(url)
    if response.status_code != 200:
        return f"❌ Docs 请求失败: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "Aave Docs"

    text = soup.get_text(separator="\n")
    doc_file = docs_path / "aave_docs_homepage.txt"
    with open(doc_file, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{text}")

    return f"✅ Aave Docs 已保存：{doc_file}"

# -----------------------------
# Part 2: 下载 GitHub 上 Aave 的审计报告 PDF
# -----------------------------
def download_audits():
    base_repo = "https://github.com/aave/audits"
    api_url = "https://api.github.com/repos/aave/audits/contents"

    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return f"❌ Audit Repo 获取失败: {response.status_code}"

    audit_files = response.json()
    downloaded = 0
    for file in audit_files:
        if file["name"].endswith(".pdf"):
            pdf_url = file["download_url"]
            pdf_name = file["name"]
            pdf_path = audits_path / pdf_name
            pdf_data = requests.get(pdf_url)
            with open(pdf_path, "wb") as f:
                f.write(pdf_data.content)
            downloaded += 1

    return f"✅ 共下载 {downloaded} 份审计报告至 {audits_path}"

# -----------------------------
# Part 3: 抓取治理论坛提案标题和链接
# -----------------------------
def fetch_governance_topics():
    url = "https://governance.aave.com/c/governance/6"
    response = requests.get(url)
    if response.status_code != 200:
        return f"❌ 治理论坛请求失败: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    topics = soup.find_all("a", class_="title raw-link raw-topic-link")
    if not topics:
        return "⚠️ 未找到治理提案"

    with open(governance_path / "topics.txt", "w", encoding="utf-8") as f:
        for topic in topics[:10]:  # 限制前10条
            title = topic.get_text(strip=True)
            link = "https://governance.aave.com" + topic["href"]
            f.write(f"{title}\n{link}\n\n")

    return f"✅ 已保存前 10 条提案到 {governance_path / 'topics.txt'}"

# -----------------------------
# 执行主流程
# -----------------------------
if __name__ == "__main__":
    print(fetch_docs_homepage())
    print(download_audits())
    print(fetch_governance_topics())

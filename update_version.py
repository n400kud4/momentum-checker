#!/usr/bin/env python3
"""
バージョン情報更新スクリプト
新しいコミット・タグ作成時にVERSION.mdを自動更新
"""

import subprocess
import re
from datetime import datetime

def get_git_info():
    """Git情報を取得"""
    try:
        # 最新タグを取得
        latest_tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], 
                                           stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError:
        latest_tag = "v1.0.0"
    
    # 現在のコミットハッシュ
    commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
    
    # 現在のブランチ
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
    
    # コミット数
    commit_count = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD']).decode().strip()
    
    return {
        'version': latest_tag,
        'commit_hash': commit_hash,
        'branch': branch,
        'commit_count': commit_count,
        'date': datetime.now().strftime('%Y年%m月%d日')
    }

def update_version_md(git_info):
    """VERSION.mdを更新"""
    current_section = f"""# バージョン情報

## 📱 現在のバージョン

### 🏷️ **バージョン**: {git_info['version']}
- **リリース日**: {git_info['date']}
- **ブランチ**: {git_info['branch']}
- **コミットハッシュ**: `{git_info['commit_hash']}`
- **コミット数**: {git_info['commit_count']}

---

## 📋 バージョン履歴

### v1.0.0 (2025-06-27) - 初回リリース
**🎯 主要機能**
- 基本モメンタム戦略実装（IEF → TQQQ/GLD判定）
- Streamlitウェブインターフェース
- 3ヶ月リバランスバックテスト機能
- CSV出力・パフォーマンス統計
- 接続エラー対策・再試行ロジック

**📁 含まれるファイル**
- `app.py` - メインアプリケーション
- `app_simple.py` - 接続最適化版
- `requirements.txt` - 依存関係
- `CLAUDE.md` - プロジェクト仕様書
- `ROADMAP.md` - 開発計画
- `direct_test.py` - データ取得テスト

**🔧 技術仕様**
- Python 3.8+
- Streamlit >= 1.28.0
- yfinance >= 0.2.20
- 月次OHLCデータ使用
- 3ヶ月リバランス戦略

---

## 🚀 次回リリース予定

### v1.1.0 (予定)
- [ ] 累積リターンチャートの追加
- [ ] リバランス頻度調整機能
- [ ] パフォーマンス指標の拡張

### v1.2.0 (予定)
- [ ] 複数銘柄対応
- [ ] リスク分析機能
- [ ] データベース統合

---

## 📞 iPhone確認用

**現在**: {git_info['version']} 
**状態**: 安定版・本番利用可能  
**最終更新**: {git_info['date']}  

---

*このファイルは新しいコミット・タグ作成時に自動更新されます*"""

    with open('VERSION.md', 'w', encoding='utf-8') as f:
        f.write(current_section)
    
    print(f"✅ VERSION.md を更新しました")
    print(f"📱 現在のバージョン: {git_info['version']}")
    print(f"🔧 コミット: {git_info['commit_hash']}")

if __name__ == "__main__":
    git_info = get_git_info()
    update_version_md(git_info)
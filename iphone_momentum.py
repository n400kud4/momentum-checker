#!/usr/bin/env python3
"""
iPhone用 ETF Momentum Checker
Pythonista 3 で実行するための軽量版
"""

import datetime

def show_header():
    """ヘッダー表示"""
    print("📱 ETF Momentum Checker")
    print("=" * 40)
    print()

def show_version():
    """バージョン情報を表示"""
    print("🏷️ バージョン情報")
    print("-" * 20)
    print("バージョン: v1.0.0")
    print("リリース日: 2025年6月27日")
    print("コミット: 1815a41")
    print("状態: 安定版・本番利用可能")
    print()

def show_current_recommendation():
    """現在の推奨銘柄（例）"""
    print("🎯 現在の推奨銘柄")
    print("-" * 20)
    print("推奨ETF: TQQQ")
    print("IEFリターン: +0.50%")
    print("判定期間: 2024/11/01 ～ 2024/12/01")
    print("判定ロジック: IEF正のモメンタム → TQQQ選択")
    print()

def show_sample_backtest():
    """サンプルバックテスト結果"""
    print("📊 サンプルバックテスト結果（2023年）")
    print("-" * 40)
    
    # サンプルデータ
    results = [
        ("2023-01", "TQQQ", "$25.50", "$32.10", "+25.9%"),
        ("2023-04", "GLD", "$180.20", "$175.80", "-2.4%"),
        ("2023-07", "TQQQ", "$28.90", "$31.40", "+8.7%"),
        ("2023-10", "GLD", "$185.50", "$191.20", "+3.1%")
    ]
    
    print(f"{'期間':<8} {'銘柄':<6} {'開始価格':<8} {'終了価格':<8} {'損益率':<8}")
    print("-" * 50)
    
    for period, etf, start, end, return_rate in results:
        print(f"{period:<8} {etf:<6} {start:<8} {end:<8} {return_rate:<8}")
    
    print()
    print("📈 統計情報")
    print("平均リターン: +8.8%")
    print("勝率: 75.0%")
    print("最大利益: +25.9%")
    print("最大損失: -2.4%")
    print()

def show_strategy_info():
    """戦略情報"""
    print("⚙️ 戦略情報")
    print("-" * 20)
    print("戦略名: IEFモメンタム戦略")
    print("リバランス: 3ヶ月ごと")
    print("判定指標: IEF 1ヶ月リターン")
    print("選択銘柄: TQQQ（正）/ GLD（負）")
    print("データソース: yfinance（月次OHLC）")
    print()

def calculate_simple_return():
    """簡単なリターン計算"""
    print("🧮 簡易リターン計算")
    print("-" * 20)
    
    try:
        start_price = float(input("開始価格を入力: $"))
        end_price = float(input("終了価格を入力: $"))
        
        return_rate = ((end_price - start_price) / start_price) * 100
        profit_loss = end_price - start_price
        
        print(f"\n結果:")
        print(f"開始価格: ${start_price:.2f}")
        print(f"終了価格: ${end_price:.2f}")
        print(f"損益: ${profit_loss:+.2f}")
        print(f"リターン: {return_rate:+.2f}%")
        
    except ValueError:
        print("❌ 正しい数値を入力してください")
    print()

def show_etf_info():
    """ETF情報"""
    print("📋 対象ETF情報")
    print("-" * 20)
    print("🔹 TQQQ (ProShares UltraPro QQQ)")
    print("   - NASDAQ 100の3倍レバレッジ")
    print("   - 高リスク・高リターン")
    print()
    print("🔹 GLD (SPDR Gold Trust)")
    print("   - 金価格連動ETF")
    print("   - インフレヘッジ・安全資産")
    print()
    print("🔹 IEF (iShares 7-10 Year Treasury)")
    print("   - 中期米国債ETF")
    print("   - モメンタム判定指標")
    print()

def main_menu():
    """メインメニュー"""
    while True:
        show_header()
        print("📋 メニュー")
        print("1. バージョン情報")
        print("2. 現在の推奨銘柄")
        print("3. サンプルバックテスト")
        print("4. 戦略情報")
        print("5. ETF情報")
        print("6. 簡易リターン計算")
        print("7. 終了")
        print()
        
        try:
            choice = input("選択してください (1-7): ").strip()
            print()
            
            if choice == "1":
                show_version()
            elif choice == "2":
                show_current_recommendation()
            elif choice == "3":
                show_sample_backtest()
            elif choice == "4":
                show_strategy_info()
            elif choice == "5":
                show_etf_info()
            elif choice == "6":
                calculate_simple_return()
            elif choice == "7":
                print("👋 ETF Momentum Checker を終了します")
                break
            else:
                print("❌ 1-7の数字を入力してください")
                print()
                continue
            
            input("📱 Enterキーで戻る...")
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 ETF Momentum Checker を終了します")
            break
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            input("📱 Enterキーで戻る...")

def pythonista_main():
    """Pythonista 3 専用メイン関数"""
    try:
        import console
        console.clear()
        
        # Pythonista 3 用の改良版メニュー
        while True:
            console.clear()
            print("📱 ETF Momentum Checker")
            print("=" * 30)
            
            choice = console.input_alert(
                "メニュー選択",
                "実行したい機能を選択してください",
                ["バージョン情報", "推奨銘柄", "バックテスト", "戦略情報", "終了"]
            )
            
            if choice == "バージョン情報":
                console.clear()
                show_version()
                console.input_alert("確認", "バージョン情報を確認しました", ["OK"])
                
            elif choice == "推奨銘柄":
                console.clear()
                show_current_recommendation()
                console.input_alert("確認", "推奨銘柄を確認しました", ["OK"])
                
            elif choice == "バックテスト":
                console.clear()
                show_sample_backtest()
                console.input_alert("確認", "バックテスト結果を確認しました", ["OK"])
                
            elif choice == "戦略情報":
                console.clear()
                show_strategy_info()
                console.input_alert("確認", "戦略情報を確認しました", ["OK"])
                
            elif choice == "終了":
                break
                
    except ImportError:
        # Pythonista 3 でない場合は通常版を実行
        main_menu()

if __name__ == "__main__":
    # Pythonista 3 の場合は専用版、それ以外は通常版
    try:
        import console
        pythonista_main()
    except ImportError:
        main_menu()
import os
from dotenv import load_dotenv
import streamlit as st
import pyperclip
import openai
import datetime

# OpenAI APIキーを設定する
openai.api_key = secrets['openai']['api_key']


# session_stateを初期化
if 'description' not in st.session_state:
    st.session_state['description'] = ''


# カスタムCSSの追加
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0; /* 背景色をグレーに設定 */
            font-family: "Arial", sans-serif; /* フォントをArialに設定 */
        }
        .stTextInput>div>div>input {
            background-color: #ffffff; /* テキスト入力フィールドの背景色を白に設定 */
            border-radius: 5px; /* テキスト入力フィールドの角丸を設定 */
            width: 100%; /* フィールドの幅を100%に設定 */
            box-sizing: border-box; /* 幅の設定を調整 */
        }
        .social-spark {
            background: linear-gradient(to right, #ff9900, #ff66cc); /* グラデーションの設定 */
            -webkit-background-clip: text; /* テキストにグラデーションを適用 */
            -webkit-text-fill-color: transparent; /* テキストの色を透明に設定 */
        }
        .submit-button {
            background: linear-gradient(to right, #ff9900, #ff66cc); /* グラデーションの設定 */
            color: white; /* 文字色を白に設定 */
            border: none; /* ボーダーをなしに設定 */
            border-radius: 5px; /* ボタンの角丸を設定 */
            padding: 8px 16px; /* パディングを設定 */
            cursor: pointer; /* マウスカーソルをポインターに設定 */
        }
        .cancel-button {
            background-color: #ff0000; /* 赤色に設定 */
            color: white; /* 文字色を白に設定 */
            border: none; /* ボーダーをなしに設定 */
            border-radius: 5px; /* ボタンの角丸を設定 */
            padding: 8px 16px; /* パディングを設定 */
            cursor: pointer; /* マウスカーソルをポインターに設定 */
        }
        .center-text {
            text-align: center; /* 中央寄せに設定 */
        }
        .generated-caption {
            padding: 10px;
            border-radius: 5px;
            background-color: #f9f9f9;
            margin-top: 20px;
            font-size: 16px;
            white-space: pre-wrap; /* テキストの折り返しを許可 */
        }
        .title-text {
            font-size: 66px; /* タイトルのフォントサイズを大きく */
            text-align: center; /* 中央寄せに設定 */
            color: #ffffff; /* タイトルの色を青色に設定 */
            background-image: linear-gradient(90deg, rgba(61, 200, 194, 1), rgba(61, 156, 194, 1) 50%, rgba(197, 125, 233, 1)); /* グラデーションの設定 */
        }
        .subheader-text {
            font-size: 24px; /* サブタイトルのフォントサイズを大きく */
            text-align: center; /* 中央寄せに設定 */
        }
        .button-container {
            display: flex; /* ボタンを横並びに */
            justify-content: flex-end; /* ボタンを右寄せに */
            margin-top: 20px; /* 上部に余白を追加 */
        }
        .button-container button {
            margin: 0 10px; /* ボタン間の間隔を追加 */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# タイトルとサブタイトルを表示
st.markdown('<div class="center-text">', unsafe_allow_html=True)
st.markdown('<h1 class="title-text">SocialSpark</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subheader-text">Your Ultimate SNS Caption Generator<br>SNSキャプション作成ツール</h2>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# session_stateを初期化
if 'session_state' not in st.session_state:
    st.session_state['session_state'] = {
        'description': '',
        'count': '',
        'place': '',
        'start_date': datetime.date.today(),
        'atmosphere': [],
        'sns': '',
        'detail': ''  # 定型文のフィールドを「詳細」に変更
    }

with st.form(key='caption_form'):
    # フォームの値をsession_stateにバインド
    st.session_state['session_state']['description'] = st.text_area('どんな投稿？', value=st.session_state['session_state']['description'], max_chars=1000)
    # 文字数のフィールドに「+」ボタンを追加
    st.session_state['session_state']['count'] = st.number_input('文字数', value=int(st.session_state['session_state']['count']) if st.session_state['session_state']['count'] else None, format="%d", min_value=0)
    st.session_state['session_state']['place'] = st.text_input('場所', value=st.session_state['session_state']['place'])

    start_date = st.date_input(
        '日付',
        value=st.session_state['session_state']['start_date']  # session_stateを参照
    )

    st.session_state['session_state']['atmosphere'] = st.multiselect(
        '投稿テイスト',
        ('真面目', '楽しく', '読みやすく', '詳細に', '簡潔に', '宣伝', '絵文字', 'ハッシュタグ','高級感','キャッチーな','富裕層向け','20代向け','30代向け','40代向け','商品説明'),
        default=[]
    )

    sns_options = ['X', 'Instagram', 'Facebook', 'YouTube']
    st.session_state['session_state']['sns'] = st.selectbox('SNSを選択してください', sns_options, index=sns_options.index(st.session_state['session_state']['sns']) if st.session_state['session_state']['sns'] in sns_options else 0)  # session_stateを参照
    
    st.session_state['session_state']['detail'] = st.text_area('詳細', value=st.session_state['session_state']['detail'], max_chars=1000)  # 定型文のフィールドを「詳細」に変更
    
    st.markdown('<div class="button-container">', unsafe_allow_html=True) # ボタンを横並びにするコンテナ開始
    submit_btn = st.form_submit_button('生成')  # クラスは適用しない
    cancel_btn = st.form_submit_button('クリア')  # クラスは適用しない
    st.markdown('</div>', unsafe_allow_html=True) # ボタンを横並びにするコンテナ終了
    
    if submit_btn:
        # SNSに対応する文体のリストを作成
        sns_styles = {
            'X': '投稿とコメント',
            'Instagram': '写真のキャプション',
            'Facebook': '投稿とコメント',
            'YouTube': 'ビデオのキャプション'
        }
        
        # 選択されたSNSに対応する文体のリストを作成
        selected_style = sns_styles[st.session_state['session_state']['sns']]
        
        # OpenAIのGPT-3モデルを使用してキャプションを生成
        prompt = f"Generate a social media caption for '{st.session_state['session_state']['description']}' with the following atmosphere: {', '.join(st.session_state['session_state']['atmosphere'])}. "
        prompt += f"It was taken on {start_date.strftime('%Y-%m-%d')} at {st.session_state['session_state']['place']} for {selected_style}."
        
        # 追加: 詳細を追加
        if st.session_state['session_state']['detail']:
            prompt += f" Additionally, {st.session_state['session_state']['detail']}."
        
        response = openai.Completion.create(  # v1/chat/completionsエンドポイントを使用
           model="gpt-3.5-turbo-1106",  # 推奨されるモデルに変更
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        generated_caption = response.choices[0].message['content'].strip()  # レスポンスからテキストを取得
        
        # 追加: 詳細を生成された文章の末尾に追加（改行あり）
        generated_caption += f"\n{st.session_state['session_state']['detail']}" 
        
        # クリップボードに生成された文章をコピー
        pyperclip.copy(generated_caption)

        # 改行を挿入して読みやすさを向上させる
        generated_caption_lines = generated_caption.split(". ")
        formatted_caption = "<br>".join(generated_caption_lines)

        st.markdown('<div class="generated-caption">{}</div>'.format(formatted_caption), unsafe_allow_html=True)

    if cancel_btn:
        # 詳細以外のフィールドを空にする
        st.session_state['session_state']['description'] = ''
        st.session_state['session_state']['count'] = ''
        st.session_state['session_state']['place'] = ''
        st.session_state['session_state']['start_date'] = datetime.date.today()
        st.session_state['session_state']['atmosphere'] = []
        st.session_state['session_state']['sns'] = ''

import streamlit as st
import pandas as pd
import datetime
import requests
import json
import os
import random

# Welcome Section
st.title("🧠 MindEase+ Mental Wellness Assistant")
st.markdown("## ✨ Welcome to Happy Club 💙")
st.write("Hey there, sunshine! 🌻")
st.markdown("""
This is your corner of calm in a busy world.  
Here, you don’t have to pretend — your feelings are valid, your voice matters, and your heart is safe. 💌  
Whether you need a cheerleader, a listener, or just a gentle reminder that you’re doing your best — I’ve got you. 🌈  
Let’s create moments of peace, joy, and self-love together. 💫
""")

st.write("---")  # Horizontal separator

# Mood Input
mood = st.text_input("🌼 Share how you're feeling today:")

if mood:
    st.success(f"✅ Mood saved! You said: *{mood}*")

    # Support Options
    st.write("💡 Choose how I can support you today:")
    option = st.radio(
        "Options:",
        [
            "Chat with Assistant",
            "Positive Affirmation",
            "Guided Meditation",
            "Fun Game 🎲",
            "Classic Riddles ❓"
        ]
    )

    if option == "Positive Affirmation":
        st.info("🌸 You are stronger than you think, and every day you’re making progress.")

    elif option == "Guided Meditation":
        st.info("🧘‍♀️ Close your eyes, take a deep breath, and count slowly to 5...")

    elif option == "Chat with Assistant":
        user_msg = st.text_area("💬 What’s on your mind?")
        if user_msg:
            with st.spinner("Thinking..."):
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "gemma:2b", "prompt": user_msg},
                )
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        resp_json = json.loads(line.decode("utf-8"))
                        if "response" in resp_json:
                            full_response += resp_json["response"]

                if full_response.strip():
                    st.write(f"💬 **Assistant:** {full_response.strip()}")

    elif option == "Fun Game 🎲":
        st.subheader("🎲 Fun Dice Roll Game")
        st.write("Roll a dice and try your luck!")

        if st.button("Roll the Dice"):
            dice_roll = random.randint(1, 6)
            st.success(f"You rolled a {dice_roll} 🎲")

    elif option == "Classic Riddles ❓":
        st.subheader("🧩 Classic Riddle Game")

        riddles = {
            "What has to be broken before you can use it?": ("egg", "It's something you eat in breakfast."),
            "I’m tall when I’m young, and I’m short when I’m old. What am I?": ("candle", "It burns and melts away."),
            "What month of the year has 28 days?": ("all", "Think carefully — every month has this many days."),
            "What is full of holes but still holds water?": ("sponge", "You use it in the bathroom or kitchen."),
            "What question can you never answer yes to?": ("are you asleep", "You can’t say yes while doing it."),
            "What has hands but can’t clap?": ("clock", "It hangs on a wall or sits on a table.")
        }

        if "classic_score" not in st.session_state:
            st.session_state.classic_score = 0
            question, answer_hint = random.choice(list(riddles.items()))
            st.session_state.current_classic_riddle, (st.session_state.classic_answer, st.session_state.classic_hint) = question, answer_hint
            st.session_state.classic_feedback = ""
            st.session_state.reset_riddle_input = False

        if st.session_state.classic_score >= 5:
            st.balloons()
            st.success("🎊 Incredible! You solved 5 Riddles! You're a genius 🧠🏅")
        else:
            st.write(f"🤔 Riddle: **{st.session_state.current_classic_riddle}**")

            default_val = "" if st.session_state.get("reset_riddle_input", False) else st.session_state.get("classic_guess", "")
            user_guess = st.text_input("Your Answer to the Riddle:", key="classic_guess_input", value=default_val).lower()

            if st.button("Submit Riddle Answer"):
                if user_guess == st.session_state.classic_answer:
                    st.session_state.classic_feedback = "🎉 Correct! You’re smart!"
                    st.session_state.classic_score += 1
                else:
                    st.session_state.classic_feedback = "❌ Not quite. Try again!"
                st.session_state.reset_riddle_input = False

            if st.button("💡 Hint (-1 point)"):
                st.session_state.classic_feedback = f"Hint: {st.session_state.classic_hint}"
                st.session_state.classic_score = max(0, st.session_state.classic_score - 1)

            if st.button("✅ Show Answer (-1 point)"):
                st.session_state.classic_feedback = f"The answer is: **{st.session_state.classic_answer}**"
                st.session_state.classic_score = max(0, st.session_state.classic_score - 1)

            if st.session_state.classic_feedback:
                st.info(st.session_state.classic_feedback)
                st.write(f"🏆 Your Score: {st.session_state.classic_score}")

            if st.button("Next Riddle ➡️"):
                question, answer_hint = random.choice(list(riddles.items()))
                st.session_state.current_classic_riddle, (st.session_state.classic_answer, st.session_state.classic_hint) = question, answer_hint
                st.session_state.classic_feedback = ""
                st.session_state.reset_riddle_input = True

else:
    st.info("🌼 Please enter how you're feeling to get started.")

# filter_config.py

# Phrases to remove from transcript for distillation (filler, fluff, low-signal)
banned_phrases = [
    # Engagement bait / filler
    "subscribe", "like the video", "follow me", "leave a comment", "smash that", "don't forget",

    # Intro/outro fluff
    "hi everyone", "hey guys", "thank you for watching", "thanks for watching", "welcome back",
    "before we get started", "with that being said", "let's get into it", "now that we've covered that",

    # Weak confirmations
    "does that make sense", "i hope that makes sense", "are you with me", "do you understand",
    "you get what i'm saying", "you see what i mean", "you feel me",

    # Empty transition phrases
    "i'm going to show you", "let me show you", "look at this", "notice how", "as you can see",
    "i want you to notice", "here’s what happens", "keep that in mind", "pay attention", "moving on",

    # Soft guidance
    "we're going to look at", "i'm going to teach you", "we're going to talk about", "what we're looking for",
    "we'll talk about", "we'll discuss", "what i want you to do",

    # Verbal padding
    "okay", "so", "again", "alright", "right", "basically", "literally", "honestly", "essentially", "actually",
    "kinda", "sort of", "you know", "just like", "a little bit",

    # Overused pacing
    "what does that mean", "in other words", "it's important to understand", "the thing is",
    "this is where it gets interesting"
]

# Threshold for minimum number of words per transcript line
min_words = 5


    # General Trading + ICT keywords
keywords = [
    # General
    "entry", "exit", "stop loss", "take profit", "risk", "risk management",
    "reward to risk", "position sizing", "leverage", "margin", "slippage",
    "spread", "order execution", "breakout", "pullback", "fakeout",
    "rejection", "bounce", "support", "resistance", "trend", "range",
    "trendline", "price action", "candle close", "wick", "engulfing pattern",
    "pin bar", "doji", "order flow", "volume", "volatility", "market depth"
    # ICT
    "liquidity sweep", "stop raid", "stop hunt", "fair value gap", "FVG",
    "optimal trade entry", "OTE", "breaker block", "order block",
    "displacement", "judas swing", "power of three", "accumulation",
    "manipulation", "distribution", "dealing range", "PD array",
    "imbalance", "market structure shift", "internal liquidity",
    "external liquidity", "supply and demand zone", "SMT divergence",
    "smart money", "buy side liquidity", "sell side liquidity",
    "high resistance liquidity", "low resistance liquidity",
    "market maker", "kill zone", "london kill zone", "new york kill zone",
    "asian range", "session open", "daily high", "daily low",
    "weekly open", "weekly high", "weekly low",

    # Indicators and analysis tools
    "moving average", "exponential moving average", "RSI", "MACD",
    "bollinger bands", "stochastic", "fibonacci retracement",
    "fibonacci extension", "VWAP", "pivot points", "divergence"

    # Institutional Concepts
    "liquidity engineering", "algorithmic sweep", "market inefficiency",
    "inefficiency fill", "sponsored move", "premium", "discount",
    "volume imbalance", "risk event", "interest rate decision",
    "news catalyst", "CPI", "NFP", "FOMC", "institutional bias",
    "session high", "session low", "time-based entry", "session close"

]
@app.post("/chat/analyze")
def analyze_session(request: dict):
    """
    Generate analysis from chat session
    """
    try:
        session_data = request.get("session_data", {})
        messages = session_data.get("messages", [])
        difficulty = session_data.get("difficulty", "intermediate")
        
        # Calculate score based on correctness
        # We look for AI messages that have the 'is_correct' flag
        ai_responses = [msg for msg in messages if msg.get("role") == "ai" and "is_correct" in msg]
        
        if ai_responses:
            total_questions = len(ai_responses)
            correct_count = 0
            for msg in ai_responses:
                is_correct = msg.get("is_correct")
                if is_correct is True:
                    correct_count += 1
                elif isinstance(is_correct, str) and is_correct.lower() == "true":
                    correct_count += 1
            print(f"DEBUG: Calculated score - Correct: {correct_count}/{total_questions}")
        else:
            # Fallback for sessions without flags
            # Count user messages as attempts
            user_messages = [msg for msg in messages if msg.get("role") == "user"]
            total_questions = len(user_messages)
            correct_count = 0
            for msg in messages:
                if msg.get("role") == "ai":
                    content = msg.get("content", "").lower()
                    # Strict heuristic: must contain "correct" and NOT "incorrect"
                    if "correct" in content and "incorrect" not in content:
                        correct_count += 1
        
        if total_questions == 0:
            overall_score = 0
        else:
            overall_score = int((correct_count / total_questions) * 100)
        
        # Generate AI-powered analysis
        analysis_prompt = f"""
        Analyze this learning session:
        Difficulty: {difficulty}
        Questions answered: {total_questions}
        Estimated correct: {correct_count}
        
        Provide:
        1. 2-3 specific strengths
        2. 2-3 areas to improve
        3. 3-4 actionable recommendations
        
        Output JSON:
        {{
            "strengths": ["...", "..."],
            "weaknesses": ["...", "..."],
            "recommendations": ["...", "...", "..."]
        }}
        """
        
        try:
            ai_analysis = chat_agent._generate(analysis_prompt)
            return {
                "overall_score": overall_score,
                **ai_analysis
            }
        except:
            return {
                "overall_score": overall_score,
                "strengths": [
                    "Good engagement with the material",
                    "Thoughtful responses to questions"
                ],
                "weaknesses": [
                    "Could benefit from more practice",
                    "Review fundamental concepts"
                ],
                "recommendations": [
                    f"Continue practicing at {difficulty} level",
                    "Review topics covered in this session",
                    "Try a more challenging difficulty next time"
                ]
            }
    except Exception as e:
        print(f"Analysis error: {e}")
        return {
            "overall_score": 0,
            "strengths": ["Good effort", "Active participation"],
            "weaknesses": ["Need more practice"],
            "recommendations": ["Keep practicing", "Review the basics"]
        }

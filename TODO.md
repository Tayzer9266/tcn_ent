# TODO List for Adding Calendar to Home Page

✅ **1. Install streamlit-calendar**:
   - Added `streamlit-calendar` to the requirements.txt file.
   - Successfully installed the package.

2. **Modify Home.py**:
   - Import the `streamlit-calendar` package.
   - Create a function to fetch all scheduled dates for the current month.
   - Add the calendar component next to the "Upcoming Events" section.
   - Highlight scheduled dates in red and unscheduled dates in green.

3. **Test the Implementation**:
   - Verify that the calendar displays correctly.
   - Ensure that the highlighting of dates works as intended.
   - Check the layout to ensure it is responsive and visually appealing.

# Claudia.ai Integration with BlackboxAI

## Next Steps

1. Set your Claudia.ai API key as an environment variable:
   - On Windows (cmd):
     ```
     set CLAUDIA_AI_API_KEY=your_api_key_here
     ```
   - On Linux/macOS (bash):
     ```
     export CLAUDIA_AI_API_KEY=your_api_key_here
     ```

2. Create and activate a Python virtual environment (optional but recommended):
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Linux/macOS
   ```

3. Install required dependencies:
   ```
   pip install requests
   ```

4. Run the example integration script:
   ```
   python claudia_ai_integration_example.py
   ```

5. Modify the script as needed to integrate with your BlackboxAI workflows.

This completes the initial integration setup.

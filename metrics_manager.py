def initialize_metrics(session_state):
    """Initialize metrics in the session state."""
    if 'response_times' not in session_state:
        session_state.response_times = []
    if 'feedback' not in session_state:
        session_state.feedback = []

def add_response_time(session_state, time):
    """Add a new response time to the metrics."""
    session_state.response_times.append(time)

def add_feedback(session_state, feedback):
    """Add new feedback to the metrics."""
    session_state.feedback.append(feedback)

def calculate_accuracy(session_state):
    """Calculate and return the accuracy based on user feedback."""
    if session_state.feedback:
        positive_feedback = session_state.feedback.count("Yes")
        total_feedback = len(session_state.feedback)
        return (positive_feedback / total_feedback) * 100
    return 0

def get_response_times(session_state):
    """Return all recorded response times."""
    return session_state.response_times

def clear_metrics(session_state):
    """Clear all metrics from the session state."""
    session_state.response_times = []
    session_state.feedback = []
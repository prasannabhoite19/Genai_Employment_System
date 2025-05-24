import spacy

nlp = spacy.load('en_core_web_sm')

job_keywords = [
    "data analyst", "data science", "software engineer", "developer", "AI"
    "data scientist", "pharmacy", "pharmacist", "nurse", "manager", "designer"
]

known_locations = [
    "pune", "mumbai", "bangalore", "delhi", "chennai", "hyderabad",
    "kolkata", "noida", "gurgaon", "india", "remote", "canada", "germany"
]

def extract_job_inputs(text):
    """
    Extract job title and location from user's natural language input.
    returns (job_title, job_location)

    """
    doc = nlp(text)
    job_title = None
    location = None

    # Using NER to detect location
    for ent in doc.ents:
        if ent.label_ == "GPE":  #Geopolitical Entity = location
            location = ent.text

    text_lower = text.lower()
    if not location:
        for city in known_locations:
            if city in text_lower:
                location = city.title()
                break

    for phrase in job_keywords:
        if phrase in text_lower:
            job_title = phrase
            break

    if not job_title and not location:
        return ("Please specifiy field in which you are looking for jobs.",
                "In which locations you are looking for jobs?")
    
    if not job_title:
        return ("Please specify the field in which you're looking for jobs.", location or "India")

    if not location:
        location = "India"

    return job_title, location


if __name__ == "__main__":
    examples = [
        "I want a pharmacy job in Pune",
        "Looking for a data analyst role in Mumbai",
        "Suggest data science jobs in India",
        "Find developer jobs",
        "Any nurse jobs in Delhi?",
        "Jobs for software engineer in Bangalore",
        "Remote jobs for data scientist",
        "Give me marketing jobs",
        "Want a manager job in Canada",
        "Internship in AI in Hyderabad"
    ]

    for text in examples:
        title,loc = extract_job_inputs(text)
        print(f"Job Title : {title}, Location : {loc}")
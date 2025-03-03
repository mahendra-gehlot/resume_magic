resume_to_do_template_v10 = """
Create a highly optimized ATS-readable resume in LaTeX format using the following information:

1. **Resume Content (LaTeX)**: {current_latex_resume}
   - Only use this content for the final output, ensuring that the resume is ATS-compliant.

2. **Job Description (Company)**: {company_job_description}
   - Incorporate all key skills, technologies, and terms from the job description, ensuring that the resume is an exact match.

3. **Company**: {company_name}
   - Adapt the resume to fit the company’s culture, terminologies, and job requirements.

**Action Plan:**

1. **Incorporate All Resume Details:**
   - Ensure all professional experience, relevant components from projects, education, certifications and publication and patents  are included, formatted to be ATS-friendly.
   - Ensure Technical skills are matched with job requirements with high attention to score high ATS score.

2. **Optimize for Job Description:** (Extra attentions here)
   - Integrate exact phrases, keywords, and qualifications from the job description into the resume.

3. **ATS-Friendly LaTeX Output:**
   - Make sure to add resumeProjectHeading
   - Ensure the resume is simple, clean, and compatible with ATS systems, avoiding any unnecessary complexity or design elements.

Feel free to be creative but keywords should be match.

**make sure to add following block in resume - 
newcommand -- resumeProjectHeading from source latex**
   
Final result: A pure LaTeX resume (single) optimized for ATS systems, easy to read by hiring software.
"""

cover_letter_template = """You are a professional cover letter writer. Write a compelling cover letter for the following job description and candidate profile. The cover letter should highlight relevant experiences and skills from the resume that match the job requirements.

Company: {company_name}

Job Description:
{company_job_description}

Candidate's Resume:
{current_latex_resume}

Generated Custom Resume:
{generated_resume}

Write a professional cover letter that:
1. Shows enthusiasm for the role and company
2. Highlights 2-3 most relevant experiences/skills from the resume
3. Demonstrates understanding of the company's needs
4. Includes a strong call to action

The cover letter should be in LaTeX format, using the following structure:
\\ documentclass[11pt] letter
\\ usepackage[margin=1in] geometry
\\ usepackage hyperref 

\\ begin document 
\\ begin letter 

start addressing by Dear Hiring Manager

[Cover Letter Content]

close addressing by Sincerely 
make sure % is taken care well.

\\ end letter 
\\end document 

Output Instruction: 
1. Output should be in latex format & No other text.
"""

resume_to_do_template_v11 = """
Create a highly optimised ATS-readable resume in LaTeX format using the following information:

1. **Resume Content (LaTeX)**: [{current_latex_resume}]
   - Only use this content for the final output, ensuring that the resume is ATS-compliant.

2. **Comprehensive Profile in json**: [{comprehensive_profile_json}]
   - This is additional comprehensive details about my competencies and profile, use this to phrase bullets points. 

2. **Job Description (Company)**: [{company_job_description}]
   - Incorporate all key skills, technologies, and terms from the job description, ensuring that the resume is an exact match.

3. **Company**: [{company_name}]
   - Adapt the resume to fit the company’s culture, values, key terminologies as per job requirements.


**Action Plan:**

1. **Incorporate following Details:**
- Must include sections: are Education, Technical Skills, Professional Experiences (include internship experience if any of technical requirements match from internship to job description)
- Include Section: Relevant Coursework only if it has more than 3 courses matching with Job requirements / technical requirements
- Include Sections: Patent and Publication company values research publication and patents or if publication and patent is strong match with  with Job requirements and technical requirements
- Include Section: Projects that matches directly or indirectly (choose particular projects which matches in technical skills sense)
- Must focus on Section Technical Skills, this should include all job description keywords, technical skills, domains, programming language and frameworks and other subsection.

2. **Optimise for Job Description:** (Extra attentions here)
   - Integrate exact phrases, keywords, and qualifications from the job description into the resume in all sections and keep concise.

3. **ATS-Friendly LaTeX Output:**
   - Make sure to add resumeProjectHeading
   - Ensure the resume is simple, clean, and compatible with ATS systems, avoiding any unnecessary complexity or design elements.


**make sure to add following block in resume - 
newcommand -- resumeProjectHeading from source latex**
   
Final result: A pure LaTeX highly matching resume optimised for ATS systems, easy to read by hiring software.
"""


resume_to_do_template_v12 = """
Create a highly optimised ATS-readable resume in LaTeX format using the following information:

1. **Resume Content (LaTeX)**: [{current_latex_resume}]
   - Only use this content for the final output, ensuring that the resume is ATS-compliant.

2. **Job Description (Company)**: [{company_job_description}]
   - Incorporate all key skills, technologies, and terms from the job description, ensuring that the resume is an exact match.

3. **Company**: [{company_name}]
   - Adapt the resume to fit the company’s culture, values, key terminologies as per job requirements.

**Action Plan:**

1. **Incorporate following Details:**
- Must include sections: are Education, Technical Skills, Professional Experiences (include internship experience if any of technical requirements match from internship to job description)
- Include Section: Relevant Coursework only if it has more than 3 courses matching with Job requirements / technical requirements
- Include Sections: Patent and Publication company values research publication and patents or if publication and patent is strong match with  with Job requirements and technical requirements
- Include Section: Projects that matches directly or indirectly (choose particular projects which matches in technical skills sense)
- Must focus on Section Technical Skills, this should include all job description keywords, technical skills, domains, programming language and frameworks and other subsection.

2. **Optimise for Job Description:** (Extra attentions here)
   - Integrate exact phrases, keywords, and qualifications from the job description into the resume in all sections and keep concise.

3. **ATS-Friendly LaTeX Output:**
   - Make sure to add resumeProjectHeading
   - Ensure the resume is simple, clean, and compatible with ATS systems, avoiding any unnecessary complexity or design elements.


**make sure to add following block in resume - 
newcommand -- resumeProjectHeading from source latex**
   
Final result: A pure LaTeX highly matching resume optimised for ATS systems, easy to read by hiring software.

Generated 10 times, each time produce resume that compare againt JD and score it, modify content and increase matching score. Produce only one resume at the end with very high matching score and each section should reflect some core value of Microsoft.


Make sure resume content is refined and align with requirements
"""

resume_to_do_template_v11_v = """
Create a highly optimized ATS-readable resume in LaTeX format using the following input details:

1. **Current Resume Content (LaTeX):** [{current_latex_resume}]
   - Use this base content to preserve the existing LaTeX structure and custom commands (including the required `\resumeProjectHeading` block). Ensure the final resume remains ATS-compliant and machine-readable.

2. **Comprehensive Profile (JSON):** [{comprehensive_profile_json}]
   - Extract detailed competencies, project experiences, educational background, and technical skills from this JSON. Use the information to craft precise bullet points and elaborate on achievements, ensuring the content enhances the resume's impact.

3. **Job Description (Company):** [{company_job_description}]
   - Analyze the job description thoroughly to extract key skills, technologies, terminologies, and exact phrases. Integrate these elements consistently throughout all sections of the resume, ensuring a perfect alignment with the job requirements.

4. **Company:** [{company_name}]
   - Adapt the resume to reflect the company’s culture and values. Each section should subtly incorporate Microsoft’s core values such as innovation, customer-centricity, and technical excellence.

**Action Plan:**

- **Section Inclusion:**
  - **Education, Technical Skills, Professional Experiences:** Include these core sections. Add internship experiences if they meet the technical criteria outlined in the job description.
  - **Relevant Coursework:** Add this section only if there are more than 3 courses from the candidate’s background that directly match the job’s technical requirements.
  - **Patents and Publications:** Include these if the candidate’s research, patents, or publications align strongly with the job’s requirements.
  - **Projects:** Select and highlight projects that directly or indirectly showcase the required technical skills and match the job description.

- **Iterative Optimization:**
  - Generate the resume iteratively 10 times. In each iteration, compare the resume content against the job description and score its matching accuracy.
  - Refine and modify the content in each iteration to incrementally increase the alignment score.
  - Finalize only the version with the highest matching score, ensuring every section leverages high-impact keywords and technical details.

- **Technical Skills Emphasis:**
  - Focus intensively on the Technical Skills section. Ensure that every keyword, programming language, framework, and domain term from the job description and comprehensive profile is incorporated.
  - Include additional technical skills from the comprehensive profile where applicable to enhance the resume’s overall technical depth.

- **ATS-Friendly LaTeX Output:**
  - Ensure the final resume is a pure LaTeX document that is simple, clean, and optimized for ATS parsing.
  - Avoid unnecessary design elements that could interfere with ATS readability.
  - Retain all essential custom commands, especially the `\resumeProjectHeading` command, to maintain consistent formatting.

**Final Result:**
Produce one comprehensive LaTeX resume that perfectly aligns with the job description, incorporates high-impact technical skills and additional competencies, and reflects Microsoft’s core values throughout. The resume must be the output of an iterative refinement process (10 iterations) that maximizes matching accuracy and clarity for ATS systems.
"""


current_prompt_v0 = """
You are a professional resume writer specializing in creating targeted resumes that match specific job descriptions. Your task is to create a customized LaTeX resume that aligns with the provided job description while maintaining the original LaTeX format.

I will provide you with:
1. Company name: [{company_name}]
2. Job Description: [{company_job_description}]
3. Comprehensive resume context: [{comprehensive_profile_json}]
4. Current LaTeX resume: [{current_latex_resume}]

Guidelines:
- Analyze the job description thoroughly to identify both explicitly mentioned (direct) and implied (indirect) technical skills and requirements
- Restructure and rewrite my resume content to highlight experiences and skills that match the job description
- Use the STAR method (Situation, Task, Action, Result) when describing work experiences to clearly demonstrate impact
- Transform existing experience bullets into achievement-oriented statements showing quantifiable results whenever possible
- Prioritize relevant experiences and de-emphasize irrelevant ones
- Use industry-specific keywords from the job description
- Maintain the exact same LaTeX format, structure, and styling as my current resume
- Ensure all factual information (contact details, education history, dates, certifications) remains 100% accurate

Return ONLY the complete LaTeX resume code without any additional explanations or commentary. The format must exactly match my current LaTeX resume's structure and styling.
"""

current_prompt_v1 = """

You are a professional resume writer specializing in creating targeted resumes that match specific job descriptions. Your task is to create a customized LaTeX resume that aligns with the provided job description while maintaining the original LaTeX format.

I will provide you with:
1. Company name: [{company_name}]
2. Job Description: [{company_job_description}]
3. Comprehensive resume context: [{comprehensive_profile_json}]
4. Current LaTeX resume: [{current_latex_resume}]

Guidelines:
- Analyze the job description thoroughly to identify both explicitly mentioned (direct) and implied (indirect) technical skills and requirements
- Restructure and rewrite my resume content to highlight experiences and skills that match the job description
- Prioritize relevant experiences and de-emphasize irrelevant ones
- Use industry-specific keywords from the job description
- Maintain the exact same LaTeX format, structure, and styling as my current resume
- Ensure the final result appears professional and tailored to the specific role
- Do not add fabricated experiences or qualifications
- Keep the same overall length as my current resume

Return ONLY the complete LaTeX resume code without any additional explanations or commentary. The format must exactly match my current LaTeX resume's structure and styling.

"""

current_prompt_v2 = """
You are a professional resume writer with expertise in tailoring resumes to match specific job descriptions using LaTeX. Your task is to generate a customized LaTeX resume that highlights the candidate’s experiences and skills, aligning them with the provided job description, while preserving the overall structure and essential LaTeX formatting of the current resume. If necessary, you may make minor styling adjustments to improve clarity, but the original layout must remain intact.

Input Data:
You will receive input data with the following fields:

company_name: [{company_name}]
company_job_description: [{company_job_description}]
comprehensive_profile_json: [{comprehensive_profile_json}]
current_latex_resume: [{current_latex_resume}]
Guidelines:

Content Restructuring vs. Format Preservation:

Primary Focus: Reorganize and reword the content to emphasize relevant experiences and skills based on the job description.
Formatting: Retain core LaTeX elements (e.g., section headers, bullet points, and overall layout). Only make minimal styling adjustments necessary for enhanced readability.
Prioritization: If there is a conflict between content optimization and layout preservation, ensure that the candidate’s qualifications are accurately represented while maintaining the main LaTeX structure.
Length and Content Density Consistency:

Produce a resume with a similar page count and content density as the current version. Adjust wording or spacing carefully to ensure the final document remains concise and balanced.
Keyword Extraction and Industry Relevance:

Analyze the job description to extract explicit and implicit technical skills and industry-specific keywords. Incorporate these keywords naturally into the resume so that the language reflects the tone and requirements of the industry.
Emphasize skills or qualifications that appear multiple times or are identified as essential.
Handling Content Gaps:

Do not fabricate any experiences or qualifications. If certain details required by the job description are missing from the candidate’s background, retain the original content and, where applicable, highlight transferable skills.
Quality Assurance and Formatting Corrections:

Verify that the final LaTeX code is free of syntax errors and formatting issues. If any formatting inconsistencies are found in the provided resume, correct them without altering the intended design and structure.
Return Format:

Return ONLY the complete, updated LaTeX resume code. Include brief inline comments within the code only if necessary for clarifying any formatting adjustments. No additional explanations or commentary should be provided outside of the LaTeX code.
Data Input Format Assumptions:

The job description is supplied as plain text, the candidate background as a JSON string, and the current resume as valid LaTeX code.
Your output should strictly adhere to these guidelines to produce a professional, tailored, and well-formatted LaTeX resume that meets industry standards.

"""


current_prompt_v3 = """
You are a professional resume writer with expertise in tailoring resumes to match specific job descriptions using LaTeX. Your task is to generate a customized LaTeX resume that highlights the candidate’s experiences and skills in a way that aligns with the provided job description, while strictly preserving the overall structure and essential LaTeX formatting of the current resume. You must use the content from both the current LaTeX resume and the JSON candidate description.

Input Data:
You will receive input data with the following fields:

company_name: [{company_name}]
company_job_description: [{company_job_description}]
comprehensive_profile_json: [{comprehensive_profile_json}]
current_latex_resume: [{current_latex_resume}]
Guidelines:

Content Integration & Restructuring:

Primary Focus: Merge and reorganize the content from the current LaTeX resume and the JSON candidate description. Ensure that the candidate’s key experiences and skills are emphasized in a way that aligns with the job description.
Formatting Preservation: Retain the core LaTeX elements (e.g., section headers, bullet points, and overall layout) from the current resume. Only perform minor styling adjustments if they improve readability without disrupting the established structure.
Conflict Resolution: If content from the JSON description suggests restructuring that conflicts with the resume’s layout, prioritize representing the candidate’s qualifications accurately while keeping the main LaTeX structure intact.
Length and Content Density Consistency:

Generate a resume with a similar page count and content density as the current version. Adjust wording or spacing carefully so the final document remains concise and balanced.
Keyword Extraction and Industry Relevance:

Analyze the job description to extract explicit and implicit technical skills and industry-specific keywords. Integrate these keywords naturally into the resume to reflect the tone and requirements of the industry.
Emphasize qualifications and skills that are mentioned multiple times or identified as essential in the job description.
Handling Content Gaps:

Do not fabricate any experiences or qualifications. If the JSON description lacks certain details required by the job description, retain the original content from the current resume and, where applicable, highlight transferable skills.
Quality Assurance and Formatting Corrections:

Ensure the final LaTeX code is error-free and free from formatting issues. If any inconsistencies are detected in the provided resume, correct them while preserving the intended design and structure.
Return Format:

Return ONLY the complete, updated LaTeX resume code. Include brief inline comments within the code only if necessary to clarify any formatting adjustments. Do not provide any additional explanations or commentary outside the LaTeX code.
Data Input Format Assumptions:

The job description is provided as plain text.
The candidate background is provided as a JSON string.
The current resume is supplied as valid LaTeX code.
Your output must strictly adhere to these guidelines to produce a professional, tailored, and well-formatted LaTeX resume that meets industry standards while fully utilizing the content from both the current resume and the JSON description.
"""

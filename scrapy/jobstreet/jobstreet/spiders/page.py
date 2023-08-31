import scrapy
import json

class JobstreetsearchSpider(scrapy.Spider):
    name = 'page'
    allowed_domains = ['jobstreet.co.id']
    start_urls = ['https://www.jobstreet.co.id/id/job/devops-engineer-4376698?jobId=jobstreet-id-job-4376698&sectionRank=4&token=0~72885a0a-279e-4303-8f5c-b610a57e2a2f&searchPath=%2Fid%2FPT-Tibeka-Logistik-Indonesia-jobs&fr=SRP%20View%20In%20New%20Tab']

    def parse(self, response):
        pre_data = response.xpath('//script[2]/text()').extract_first()

#         print("Raw Data:", data)  # Debugging statement to check the value of data
        data = pre_data.replace("window.REDUX_STATE = ", "") 

        if data:
            try:
                # Parse the JSON data
                json_data = json.loads(data)

                # Extract the job title
                job_title = json_data.get('jobTitle')

                # Print the job title
                print("Job Title:", job_title)
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", str(e))
        else:
            print("No data found.")

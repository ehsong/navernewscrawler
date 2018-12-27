import json
import argparse
import datetime as dt
from navernewscrawler.naver_crawler import get_news, get_dates, output
import csv

def main():
    try:
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__
        )
        parser.add_argument("query", type=str, help="query word or words separated by space")
        parser.add_argument("-max_page", "--max_page", type=int, default=5,help="number of maximum pages to crawl per date")
        parser.add_argument("-p", "--page", type=int, default=1,help="the starting page")
        parser.add_argument("-c", "--csv", action='store_true',
                                help="Set this flag if you want to save the results to a CSV format.")
        parser.add_argument("-d", "--dump", action="store_true",
                            help="Set this flag to dump the results on console")
        parser.add_argument("-bd", "--begindate", type=str, default='2018-12-26',
                            help="Scrape news starting from this date. Format YYYY-MM-DD. \nDefault value is 2018-12-26", metavar='\b')
        parser.add_argument("-ed", "--enddate", type=str, default='2018-12-26',
                            help="Scrape for news until this date. Format YYYY-MM-DD. \nDefault value is 2018-12-26.", metavar='\b')
        args = parser.parse_args()

        news_dicts = output(query = args.query ,page = args.page ,max_page = args.max_page, start_date = args.begindate, end_date = args.enddate)

        start_date = args.begindate
        end_date = args.enddate

        if args.dump:
            print(news_dicts)
        else:
            if args.csv:
                s_from = start_date.replace("-","")
                e_to = end_date.replace("-","")
                with open(s_from+"_news_scrape_"+e_to+".csv", "w", encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=news_dicts[0].keys())
                    writer.writeheader()
                    writer.writerows(news_dicts)
                    f.close()
            else:
                s_from = start_date.replace("-","")
                e_to = end_date.replace("-","")
                jsonfile = open(s_from+"_news_scrape_"+e_to+".json", 'w',encoding="utf-8")
                json.dump(news_dicts, jsonfile)
                jsonfile.close()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Quitting...")

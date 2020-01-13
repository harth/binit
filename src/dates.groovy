@groovy.lang.Grab(group = 'org.seleniumhq.selenium', module = 'selenium-java', version = '3.141.59')
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions

import java.text.SimpleDateFormat

System.setProperty('webdriver.chrome.driver', '../chromedriver');

private static ArrayList<BD> getAllBinDates(ChromeDriver browser) {
    def bds = new ArrayList<BD>();
    browser.findElementByClassName("bins").getText().split('\n').each {
        if (it.contains('Grey') || it.contains('Blue') || it.contains('Brown') || it.contains('Green') || it.contains('Glass')) {
            String[] results = it.split("([b|B]in)|Box")
            bds.add(new BD(colour: results[0].trim(), date: convertToDate(results[1].trim())))
        }
    }
    bds
}

static BD getFirstCollectionDate(ArrayList<BD> bds) {
    bds.sort { a, b -> a.date <=> b.date }.get(0)
}

static Date convertToDate(String date) {
    new SimpleDateFormat("EEEE dd MMMM yyyy").parse(date);
}

class BD {
    String colour
    Date date
}

ChromeOptions chromeOptions = new ChromeOptions();
chromeOptions.addArguments("--headless")
def browser = new ChromeDriver(chromeOptions)
browser.manage().window().maximize()
browser.get('https://www.stirling.gov.uk/bins-waste-recycling/bin-collection-dates/?uprn=122014510')

def schedule = getAllBinDates(browser)

def firstCollectionDate = getFirstCollectionDate(schedule)

println "Next collection date is ${firstCollectionDate.date}"
println "Bins to be collected"
schedule.findAll { it.date == firstCollectionDate.date }.each {println it.colour}

browser.quit()
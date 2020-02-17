import groovy.BinData
@groovy.lang.Grab(group = 'org.seleniumhq.selenium', module = 'selenium-java', version = '3.141.59')
@groovy.lang.Grab(group = 'com.fasterxml.jackson.core', module = 'jackson-databind', version = '2.10.1')
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions

import java.text.SimpleDateFormat
import java.util.concurrent.TimeUnit

static Date convertToDate(String date) {
    new SimpleDateFormat("EEEE dd MMMM yyyy").parse(date)
}


///////////////////////////////////////////////////////////////////
// Get a web browser and navigate to the first page
///////////////////////////////////////////////////////////////////
def driverLocation = (System.properties['os.name'] == 'Mac OS X') ? 'main/resources/chromedriver' : '/usr/bin/chromedriver'
System.setProperty('webdriver.chrome.driver', driverLocation)
final ChromeOptions options = new ChromeOptions()
options.addArguments("--headless")
final WebDriver driver = new ChromeDriver(options)
driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)

def dir = new File(String.format("%s/.wheelie", System.getProperty("user.home")))
if (!dir.exists()) dir.mkdirs()
def customer = new File(String.format("%s/%s", dir, "customer.json"))

driver.get(new JsonSlurper().parseText(customer.text).lookupUrl as String)

///////////////////////////////////////////////////////////////////
// Get the schedule from the Stirling council website
///////////////////////////////////////////////////////////////////

def schedule = new ArrayList<BinData>()
driver.findElementByClassName("bins").getText().split('\n').each {
    if (it.contains('Grey') || it.contains('Blue') || it.contains('Brown') || it.contains('Green') || it.contains('Glass')) {
        String[] results = it.split("((Bin & Food Caddy)|[b|B]in)|Box")
        schedule.add(new BinData(colour: results[0].trim(), collectionDate: convertToDate(results[1].trim())))
    }
}

///////////////////////////////////////////////////////////////////
// Get the first collection date
///////////////////////////////////////////////////////////////////
BinData firstCollectionDate = schedule.sort { a, b -> a.collectionDate <=> b.collectionDate }.get(0)

///////////////////////////////////////////////////////////////////
// Get all bins to be collected on the day
///////////////////////////////////////////////////////////////////
schedule.findAll { it.collectionDate == firstCollectionDate.collectionDate }.each { it.toBeCollected = true }

///////////////////////////////////////////////////////////////////
// Record the result for other scripts to read
///////////////////////////////////////////////////////////////////
def json_str = JsonOutput.toJson(schedule)
def json_beauty = JsonOutput.prettyPrint(json_str)
File file = new File(String.format("%s/%s", dir, "schedule.json"))
file.write(json_beauty)

driver.quit()
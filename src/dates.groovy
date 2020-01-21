@groovy.lang.Grab(group = 'org.seleniumhq.selenium', module = 'selenium-java', version = '3.141.59')
@groovy.lang.Grab(group = 'com.fasterxml.jackson.core', module = 'jackson-databind', version = '2.10.1')
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.remote.DesiredCapabilities
import org.openqa.selenium.remote.RemoteWebDriver

import java.text.SimpleDateFormat
import java.util.concurrent.TimeUnit

System.setProperty('webdriver.chrome.driver', '../chromedriver')

static Date convertToDate(String date) {
    new SimpleDateFormat("EEEE dd MMMM yyyy").parse(date)
}

class BinData {
    String colour
    Date collectionDate
    boolean toBeCollected
}

///////////////////////////////////////////////////////////////////
// Get a web browser and navigate to the first page
///////////////////////////////////////////////////////////////////

DesiredCapabilities capabilities = DesiredCapabilities.chrome()

def options = new ChromeOptions()
options.addArguments("disable-infobars")
capabilities.setCapability(ChromeOptions.CAPABILITY, options)

RemoteWebDriver driver = new RemoteWebDriver(capabilities)

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
        String[] results = it.split("([b|B]in)|Box")
        schedule.add(new BinData(colour: results[0].trim(), collectionDate: convertToDate(results[1].trim())))
    }
}

///////////////////////////////////////////////////////////////////
// Get the first collection date
///////////////////////////////////////////////////////////////////
def firstCollectionDate = schedule.sort { a, b -> a.collectionDate <=> b.collectionDate }.get(0)

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
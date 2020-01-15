@groovy.lang.Grab(group = 'org.seleniumhq.selenium', module = 'selenium-java', version = '3.141.59')
@groovy.lang.Grab(group = 'com.fasterxml.jackson.core', module = 'jackson-databind', version = '2.10.1')
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.SerializationFeature
import com.fasterxml.jackson.databind.util.StdDateFormat
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions

import java.text.SimpleDateFormat

System.setProperty('webdriver.chrome.driver', '../chromedriver')

private static ArrayList<BinData> getAllBinDates(ChromeDriver browser) {
    def bds = new ArrayList<BinData>()
    browser.findElementByClassName("bins").getText().split('\n').each {
        if (it.contains('Grey') || it.contains('Blue') || it.contains('Brown') || it.contains('Green') || it.contains('Glass')) {
            String[] results = it.split("([b|B]in)|Box")
            bds.add(new BinData(colour: results[0].trim(), collectionDate: convertToDate(results[1].trim())))
        }
    }
    bds
}

static BinData getFirstCollectionDate(ArrayList<BinData> bds) {
    bds.sort { a, b -> a.collectionDate <=> b.collectionDate }.get(0)
}

static Date convertToDate(String date) {
    new SimpleDateFormat("EEEE dd MMMM yyyy").parse(date)
}

static writeSchedule(ArrayList<BinData> schedule) {
    final ObjectMapper mapper = new ObjectMapper()
    mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
    mapper.setDateFormat(new StdDateFormat().withColonInTimeZone(true))

    def dir = new File(String.format("%s/.wheelie", System.getProperty("user.home")))
    if (!dir.exists()) dir.mkdirs()

    def scheduleFile = new File(String.format("%s/%s", dir, "schedule.json"))
    scheduleFile.text = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(schedule)
}

static ChromeDriver getBrowser() {
    def browser = new ChromeDriver(new ChromeOptions().addArguments("--headless"))
    browser.manage().window().maximize()
    browser.get('https://www.stirling.gov.uk/bins-waste-recycling/bin-collection-dates/?uprn=122014510')
    browser
}

class BinData {
    String colour
    Date collectionDate
    boolean toBeCollected
}

ChromeDriver browser = getBrowser()
def schedule = getAllBinDates(browser)
def firstCollectionDate = getFirstCollectionDate(schedule)
schedule.findAll { it.collectionDate == firstCollectionDate.collectionDate }.each { it.toBeCollected = true }
writeSchedule(schedule)
browser.quit()
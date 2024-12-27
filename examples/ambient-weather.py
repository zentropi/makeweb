from makeweb import App

app = App()
app.host = "0.0.0.0"
app.port = 8022
app.debug = True
app.data = None  # type: Weather


class WeatherFromStation:
    def __init__(self, **kwargs):
        self.weeklyrainin = kwargs.get("weeklyrainin")
        self.dateutc = kwargs.get("dateutc")
        self.PASSKEY = kwargs.get("PASSKEY")
        self.windgustmph = kwargs.get("windgustmph")
        self.eventrainin = kwargs.get("eventrainin")
        self.tempf = kwargs.get("tempf")
        self.hourlyrainin = kwargs.get("hourlyrainin")
        self.humidity = kwargs.get("humidity")
        self.dailyrainin = kwargs.get("dailyrainin")
        self.maxdailygust = kwargs.get("maxdailygust")
        self.totalrainin = kwargs.get("totalrainin")
        self.tempinf = kwargs.get("tempinf")
        self.baromrelin = kwargs.get("baromrelin")
        self.baromabsin = kwargs.get("baromabsin")
        self.monthlyrainin = kwargs.get("monthlyrainin")
        self.stationtype = kwargs.get("stationtype")
        self.uv = kwargs.get("uv")
        self.battout = kwargs.get("battout")
        self.winddir = kwargs.get("winddir")
        self.solarradiation = kwargs.get("solarradiation")
        self.humidityin = kwargs.get("humidityin")
        self.windspeedmph = kwargs.get("windspeedmph")
        self.yearlyrainin = kwargs.get("yearlyrainin")


class Weather:
    """Converts WeatherFromStation to metric units with humanized output."""

    def __init__(self, data: WeatherFromStation):
        self.data = data

    def fahrenheit_to_celsius(self, f: float) -> str:
        """Convert Fahrenheit to Celsius."""
        celsius = (float(f) - 32) * 5 / 9
        return f"{celsius:.1f}°C"

    def mph_to_kmph(self, mph: float) -> str:
        """Convert miles per hour to kilometers per hour."""
        kmh = float(mph) * 1.60934
        return f"{kmh:.1f} km/h"

    def inches_to_mm(self, inches: float) -> str:
        """Convert inches to millimeters."""
        mm = float(inches) * 25.4
        return f"{mm:.1f} mm"

    def inhg_to_hpa(self, inhg: float) -> str:
        """Convert inches of mercury to hectopascals."""
        hpa = float(inhg) * 33.8639
        return f"{hpa:.1f} hPa"

    def format_percentage(self, value: float) -> str:
        """Format percentage values."""
        return f"{float(value):.0f}%"

    # Temperature properties
    @property
    def temp(self) -> str:
        """Outside temperature in Celsius."""
        return self.fahrenheit_to_celsius(self.data.tempf)

    @property
    def temp_indoor(self) -> str:
        """Indoor temperature in Celsius."""
        return self.fahrenheit_to_celsius(self.data.tempinf)

    # Wind properties
    @property
    def wind_speed(self) -> str:
        """Current wind speed in km/h."""
        return self.mph_to_kmph(self.data.windspeedmph)

    @property
    def wind_gust(self) -> str:
        """Current wind gust in km/h."""
        return self.mph_to_kmph(self.data.windgustmph)

    @property
    def wind_dir(self) -> float:
        """Wind direction in degrees."""
        return self.data.winddir

    @property
    def max_daily_gust(self) -> str:
        """Maximum wind gust today in km/h."""
        return self.mph_to_kmph(self.data.maxdailygust)

    # Pressure properties
    @property
    def pressure(self) -> str:
        """Relative barometric pressure in hPa."""
        return self.inhg_to_hpa(self.data.baromrelin)

    @property
    def pressure_absolute(self) -> str:
        """Absolute barometric pressure in hPa."""
        return self.inhg_to_hpa(self.data.baromabsin)

    # Humidity properties
    @property
    def humidity(self) -> str:
        """Outside humidity percentage."""
        return self.format_percentage(self.data.humidity)

    @property
    def humidity_indoor(self) -> str:
        """Indoor humidity percentage."""
        return self.format_percentage(self.data.humidityin)

    # Rain properties
    @property
    def rain_hourly(self) -> str:
        """Hourly rainfall in mm."""
        return self.inches_to_mm(self.data.hourlyrainin)

    @property
    def rain_daily(self) -> str:
        """Daily rainfall in mm."""
        return self.inches_to_mm(self.data.dailyrainin)

    @property
    def rain_weekly(self) -> str:
        """Weekly rainfall in mm."""
        return self.inches_to_mm(self.data.weeklyrainin)

    @property
    def rain_monthly(self) -> str:
        """Monthly rainfall in mm."""
        return self.inches_to_mm(self.data.monthlyrainin)

    @property
    def rain_yearly(self) -> str:
        """Yearly rainfall in mm."""
        return self.inches_to_mm(self.data.yearlyrainin)

    @property
    def rain_event(self) -> str:
        """Current rain event amount in mm."""
        return self.inches_to_mm(self.data.eventrainin)

    @property
    def rain_total(self) -> str:
        """Total rainfall in mm."""
        return self.inches_to_mm(self.data.totalrainin)

    # Solar radiation properties
    @property
    def solar_radiation(self) -> str:
        """Solar radiation in W/m²."""
        return f"{self.data.solarradiation} W/m²"

    @property
    def uv_index(self) -> float:
        """UV index."""
        return self.data.uv

    # Station properties
    @property
    def battery(self) -> float:
        """Battery status."""
        return self.data.battout

    @property
    def station_type(self) -> str:
        """Weather station model."""
        return self.data.stationtype

    @property
    def timestamp(self) -> str:
        """Timestamp of the reading."""
        return self.data.dateutc


@app.route("/data")
def recv(request):
    weather_from_station = WeatherFromStation(**request.args)
    weather = Weather(weather_from_station)
    print("Temperature (outdoor):", weather.temp)
    print("Temperature (indoor):", weather.temp_indoor)
    print("Timestamp:", weather.timestamp)
    app.data = weather
    return "OK\n"


@app.page("/")
def index(doc, request):
    data = app.data
    with doc:
        with doc.head():
            doc.meta(charset="utf-8")
            doc.meta(name="viewport", content="width=device-width, initial-scale=1.0")
            doc.title("Weather")
            doc.style(
                """
                :root {
                    font-size: 16px;
                    --primary: #007bff;
                    --secondary: #6c757d;
                    --success: #28a745;
                    --info: #17a2b8;
                    --warning: #ffc107;
                    --danger: #dc3545;
                    --light: #f8f9fa;
                    --dark: #343a40;
                }
                *, *::before, *::after {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }
                body { 
                    font-size: 1rem;
                    font-family: sans-serif;
                    width: 100%;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 1rem;
                    background-color: var(--light);
                    color: var(--dark);
                }
                header {
                    margin-bottom: 2rem;
                    border-bottom: 1px solid #ddd;
                    display: flex;
                    justify-content: space-between;
                    align-items: baseline;
                    padding-bottom: 1rem;
                }
                header h1 {
                    font-size: 2rem;
                    color: var(--primary);
                }
                header span {
                    font-size: 0.9rem;
                    color: var(--secondary);
                }
                main {
                    display: grid;
                    grid-template-columns: 1fr;  /* Single column by default */
                    gap: 1.5rem;
                    width: 100%;
                }
                .section {
                    background: white;
                    padding: 1.5rem;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .section h2 {
                    color: var(--primary);
                    margin-bottom: 1rem;
                    font-size: 1.4rem;
                }
                .section p {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 0.5rem;
                    padding: 0.5rem 0;
                    border-bottom: 1px solid #eee;
                }
                .section p:last-child {
                    border-bottom: none;
                }
                .label {
                    color: var(--secondary);
                }
                .value {
                    font-weight: 500;
                }
                footer {
                    margin-top: 2rem;
                    padding-top: 1rem;
                    border-top: 1px solid #ddd;
                    text-align: center;
                    color: var(--secondary);
                    font-size: 0.9rem;
                }
                /* Tablet and desktop screens */
                @media (min-width: 768px) {
                    body {
                        padding: 2rem;
                    }
                    main {
                        grid-template-columns: repeat(3, 1fr);
                    }
                }
                """
            )
        with doc.body():
            with doc.header():
                with doc.div():
                    doc.h1("Ambient Weather")
                    doc.span(f"{data.timestamp} UTC", cls="value")
                with doc.div():
                    doc.progress(value=data.battery, min=0, max=1)
                    doc.br()
                    doc.span(data.station_type)

            with doc.main():
                with doc.div(cls="section"):
                    doc.h2("Temperature")
                    with doc.p():
                        doc.span("Outdoor", cls="label")
                        doc.span(data.temp, cls="value")
                    with doc.p():
                        doc.span("Indoor", cls="label")
                        doc.span(data.temp_indoor, cls="value")

                with doc.div(cls="section"):
                    doc.h2("Wind")
                    with doc.p():
                        doc.span("Speed", cls="label")
                        doc.span(data.wind_speed, cls="value")
                    with doc.p():
                        doc.span("Gust", cls="label")
                        doc.span(data.wind_gust, cls="value")
                    with doc.p():
                        doc.span("Direction", cls="label")
                        doc.span(f"{data.wind_dir}°", cls="value")
                    with doc.p():
                        doc.span("Max gust", cls="label")
                        doc.span(data.max_daily_gust, cls="value")

                with doc.div(cls="section"):
                    doc.h2("Pressure")
                    with doc.p():
                        doc.span("Relative", cls="label")
                        doc.span(data.pressure, cls="value")
                    with doc.p():
                        doc.span("Absolute", cls="label")
                        doc.span(data.pressure_absolute, cls="value")

                with doc.div(cls="section"):
                    doc.h2("Humidity")
                    with doc.p():
                        doc.span("Outdoor", cls="label")
                        doc.span(data.humidity, cls="value")
                    with doc.p():
                        doc.span("Indoor", cls="label")
                        doc.span(data.humidity_indoor, cls="value")

                with doc.div(cls="section"):
                    doc.h2("Rain")
                    with doc.p():
                        doc.span("Hourly rate", cls="label")
                        doc.span(data.rain_hourly, cls="value")
                    with doc.p():
                        doc.span("Daily", cls="label")
                        doc.span(data.rain_daily, cls="value")
                    with doc.p():
                        doc.span("Event", cls="label")
                        doc.span(data.rain_event, cls="value")

                with doc.div(cls="section"):
                    doc.h2("Solar Radiation")
                    with doc.p():
                        doc.span("Radiation", cls="label")
                        doc.span(data.solar_radiation, cls="value")
                    with doc.p():
                        doc.span("UV Index", cls="label")
                        doc.span(str(data.uv_index), cls="value")

            with doc.footer():
                doc.p("Powered by Zentropi MakeWeb")


if __name__ == "__main__":
    app.run(port=80)

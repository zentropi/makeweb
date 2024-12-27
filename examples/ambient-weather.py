from makeweb import App

app = App()
app.host = "0.0.0.0"
app.port = 8022
app.debug = True
app.data = None


class WeatherFromStation:
    def __init__(self, **kwargs):
        self.weeklyrainin = kwargs.get("weeklyrainin", 0.0)
        self.dateutc = kwargs.get("dateutc", "unknown")
        self.windgustmph = kwargs.get("windgustmph", 0.0)
        self.eventrainin = kwargs.get("eventrainin", 0.0)
        self.tempf = kwargs.get("tempf", 32.0)
        self.hourlyrainin = kwargs.get("hourlyrainin", 0.0)
        self.humidity = kwargs.get("humidity", 0.0)
        self.dailyrainin = kwargs.get("dailyrainin", 0.0)
        self.maxdailygust = kwargs.get("maxdailygust", 0.0)
        self.totalrainin = kwargs.get("totalrainin", 0.0)
        self.tempinf = kwargs.get("tempinf", 32.0)
        self.baromrelin = kwargs.get("baromrelin", 0.0)
        self.baromabsin = kwargs.get("baromabsin", 0.0)
        self.monthlyrainin = kwargs.get("monthlyrainin", 0.0)
        self.stationtype = kwargs.get("stationtype", "unknown")
        self.uv = kwargs.get("uv", 0)
        self.battout = kwargs.get("battout", 0)
        self.winddir = kwargs.get("winddir", 0.0)
        self.solarradiation = kwargs.get("solarradiation", 0.0)
        self.humidityin = kwargs.get("humidityin", 0.0)
        self.windspeedmph = kwargs.get("windspeedmph", 0.0)
        self.yearlyrainin = kwargs.get("yearlyrainin", 0.0)


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
    print("Received weather data for:", weather.timestamp)
    app.data = weather
    return "OK\n"


@app.page("/")
def index(doc, _request):
    data = app.data

    def render_card(title: str, items: dict):
        with doc.div(cls="section"):
            doc.h2(title)
            for label, value in items.items():
                with doc.p():
                    doc.span(label, cls="label")
                    doc.span(value, cls="value")

    with doc:
        with doc.head():
            doc.meta(charset="utf-8")
            doc.meta(name="viewport", content="width=device-width, initial-scale=1.0")
            doc.title("Weather")
            doc.style(
                """
                /* Theme variables */
                :root {
                    --primary: #007bff;
                    --secondary: #6c757d;
                    --success: #28a745;
                    --info: #17a2b8;
                    --warning: #ffc107;
                    --danger: #dc3545;
                    
                    /* Light theme (default) */
                    --bg-primary: #f8f9fa;
                    --bg-secondary: #ffffff;
                    --text-primary: #343a40;
                    --text-secondary: #6c757d;
                    --border-color: #ddd;
                    --card-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    --divider-color: #eee;
                    
                    font-size: 16px;
                }

                /* Dark theme */
                @media (prefers-color-scheme: dark) {
                    :root {
                        --bg-primary: #1a1a1a;
                        --bg-secondary: #2d2d2d;
                        --text-primary: #e0e0e0;
                        --text-secondary: #ababab;
                        --border-color: #404040;
                        --card-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        --divider-color: #404040;
                    }
                }

                /* Add smooth transitions */
                * {
                    transition: background-color 0.3s ease, color 0.3s ease;
                }

                /* Reset and box model */
                *, *::before, *::after {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }

                /* Layout */
                body { 
                    background-color: var(--bg-primary);
                    color: var(--text-primary);
                    width: 100%;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 1rem;
                }

                main {
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 1.5rem;
                    width: 100%;
                }

                /* Typography */
                body {
                    font-size: 1rem;
                    font-family: sans-serif;
                }

                /* Components */
                header {
                    margin-bottom: 2rem;
                    padding-bottom: 1rem;
                    border-bottom: 1px solid var(--border-color);
                    display: flex;
                    justify-content: space-between;
                    align-items: baseline;
                }

                header h1 {
                    font-size: 2rem;
                    color: var(--primary);
                }

                header span {
                    font-size: 0.9rem;
                    color: var(--text-secondary);
                }

                .section {
                    background: var(--bg-secondary);
                    padding: 1.5rem;
                    border-radius: 8px;
                    box-shadow: var(--card-shadow);
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
                    border-bottom: 1px solid var(--divider-color);
                }

                .section p:last-child {
                    border-bottom: none;
                }

                .label {
                    color: var(--text-secondary);
                }

                .value {
                    font-weight: 500;
                }

                footer {
                    margin-top: 2rem;
                    padding-top: 1rem;
                    border-top: 1px solid var(--border-color);
                    text-align: center;
                    color: var(--text-secondary);
                    font-size: 0.9rem;
                }

                /* Responsive */
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
                render_card(
                    "Temperature", {"Outdoor": data.temp, "Indoor": data.temp_indoor}
                )

                render_card(
                    "Wind",
                    {
                        "Speed": data.wind_speed,
                        "Gust": data.wind_gust,
                        "Direction": f"{data.wind_dir}°",
                        "Max gust": data.max_daily_gust,
                    },
                )

                render_card(
                    "Pressure",
                    {"Relative": data.pressure, "Absolute": data.pressure_absolute},
                )

                render_card(
                    "Humidity",
                    {"Outdoor": data.humidity, "Indoor": data.humidity_indoor},
                )

                render_card(
                    "Rain",
                    {
                        "Hourly rate": data.rain_hourly,
                        "Daily": data.rain_daily,
                        "Event": data.rain_event,
                    },
                )

                render_card(
                    "Solar Radiation",
                    {"Radiation": data.solar_radiation, "UV Index": str(data.uv_index)},
                )

            with doc.footer():
                doc.p("Built with Zentropi MakeWeb")


if __name__ == "__main__":
    app.data = Weather(WeatherFromStation())
    app.run()

import datetime
import asyncio
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import io
import base64

matplotlib.use('Agg')  # Use a non-GUI backend

# from django.conf import settings

time = datetime.datetime.now().strftime("%d_%m_%y-%H:%M")
# fig_root = settings.MEDIA_ROOT


class Draw:
    def __init__(self, data: dict = None):
        self.data = data

    async def PieChart(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = self.data.values()

            # Create Pie Chart
            plt.figure(figsize=(12, 8))
            plt.pie(percentages, labels=crops, autopct='%1.1f%%', startangle=140)
            plt.title('Crop Suitability Distribution PieChart')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # plt.show()
            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'PieChart_{time}'))
        except Exception as e:
            print(e)

    async def BarChart(self):
        try:
            crops = self.data.keys()
            percentages = self.data.values()

            # Create Bar Chart
            plt.figure(figsize=(10, 8))
            plt.bar(crops, percentages, color='skyblue')
            plt.xlabel('Crops')
            plt.ylabel('Suitability (%)')
            plt.title('Crop Suitability Comparison')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # plt.show()
            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'BarChart_{time}'))
        except Exception as e:
            print(e)

    async def StackedBarChart(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = self.data.values()

            # Create Stacked Bar Chart
            plt.figure(figsize=(10, 8))
            plt.bar(crops, percentages, color='lightgreen')
            plt.title('Crop Suitability - Stacked Bar')
            plt.xlabel('Crops')
            plt.ylabel('Suitability (%)')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # plt.show()
            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'StackedBarChart_{time}'))
        except Exception as e:
            print(e)

    async def ParetoChart(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = self.data.values()

            sorted_percentages = sorted(percentages, reverse=True)
            cumulative_percentage = np.cumsum(sorted_percentages)

            # Create Pareto Chart
            fig, ax = plt.subplots(figsize=(10, 8))

            ax.bar(crops, sorted_percentages, color='lightblue')
            ax.set_xlabel('Crops')
            ax.set_ylabel('Suitability (%)')

            # Cumulative percentage line
            ax2 = ax.twinx()
            ax2.plot(crops, cumulative_percentage,
                    color='red', marker="D", linestyle='-')
            ax2.set_ylabel('Cumulative Percentage (%)')

            plt.title('Pareto Chart of Crop Suitability')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # plt.show()
            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'ParetoChart_{time}'))
        except Exception as e:
            print(e)

    async def RadarChart(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = list(self.data.values())

            # Number of variables
            num_vars = len(crops)

            # Create Radar Chart
            angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
            percentages += percentages[:1]
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
            ax.fill(angles, percentages, color='blue', alpha=0.25)
            ax.plot(angles, percentages, color='blue', linewidth=2)

            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(crops)
            plt.title('Radar Chart of Crop Suitability')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # plt.show()
            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'RadarChart_{time}'))
        except Exception as e:
            print(e)

    async def Heatmap(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = list(self.data.values())

            # Create Heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap([percentages], annot=True, cmap='YlGnBu', cbar=False,
                        xticklabels=crops, yticklabels=['Suitability'])
            plt.title('Heatmap of Crop Suitability')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # plt.show()
            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'CreateHeatmap_{time}'))
        except Exception as e:
            print(e)

    async def FunnelChart(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = self.data.values()

            # Create Funnel Chart
            plt.figure(figsize=(10, 8))
            plt.fill_betweenx(crops, percentages, color='lightcoral', alpha=0.7)
            plt.xlabel('Suitability (%)')
            plt.ylabel('Crops')
            plt.title('Funnel Chart of Crop Suitability')
            plt.gca().invert_yaxis()

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # plt.show()
            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'FunnelChart_{time}'))
        except Exception as e:
            print(e)

    async def DoughnutChart(self):
        try:
            # Data
            crops = self.data.keys()
            percentages = self.data.values()

            # Create Doughnut Chart
            plt.figure(figsize=(12, 8))
            plt.pie(percentages, labels=crops, autopct='%1.1f%%',
                    startangle=140, wedgeprops=dict(width=0.4))
            plt.title('Doughnut Chart of Crop Suitability')

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # plt.show()
            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'DoughnutChart_{time}'))
        except Exception as e:
            print(e)

    async def LineChart(self):
        try:
            # Simulated data (e.g., crop suitability over time)
            years = self.data.keys()
            suitability = self.data.values()

            # Create Line Chart
            plt.figure(figsize=(8, 8))
            plt.plot(years, suitability, marker='o', color='green', label='Barley')
            plt.xlabel('Years')
            plt.ylabel('Suitability (%)')
            plt.title('Trend of Barley Suitability Over Time')
            plt.legend()

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Convert the buffer to a base64 string
            image_data = base64.b64encode(buf.read()).decode('utf-8')

            # plt.show()
            # Close the plot to free up memory
            plt.close()

            # Return the raw image data
            return image_data
            # plt.savefig(os.path.join(fig_root, f'LineChart_{time}'))
        except Exception as e:
            print(e)

    async def fetchAll(self):
        try:
            Bdata = await self.BarChart()
            Hdata = await self.Heatmap()
            Ddata = await self.DoughnutChart()
            Fdata = await self.FunnelChart()
            # Ldata = await self.LineChart()
            Padata = await self.ParetoChart()
            Pidata = await self.PieChart()
            Rdata = await self.RadarChart()
            Sdata = await self.StackedBarChart()

            return [Bdata, Hdata, Ddata, Fdata, Padata, Pidata, Rdata, Sdata]
        except Exception as e:
            print(e)


if __name__ == "__main__":
    async def main():
        _r_data = {
            "cotton": 77.78,
            "sunflower": 15.81,
            "orange": 11.11,
            "pepper": 7.50,
            "pigeonpeas": 5.56,
            "blackgram": 5.56,
            "cassava": 4.15,
            "cowpea": 3.53,
            "millet": 3.43,
            "peas": 2.47
            }
        init = Draw(_r_data)
        data = await init.fetchAll()
        # print(data[0])
    asyncio.run(main())

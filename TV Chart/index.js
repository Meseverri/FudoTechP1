
// Date, Time, Open, High, Low, Last, Volume, NumberOfTrades, BidVolume, AskVolume
const getData = async () => {
    const res = await fetch("6EM22-CME.scid_BarData.txt");
    const resp = await res.text();
    const cdata = resp.split('\n').map((row) => {
        const [time1, time2, open, high, low, close] = row.split(',');
        const [yyy, mm, dd] = time1.split('/');
        var [hh, min, ss] = time2.split(':');
        hh = hh.replace(" ","");
        // console.log(hh, min, ss);

        return {
          time: new Date(yyy, mm, dd, hh, min, ss).getTime() / 1000,
          open: open * 1,
          high: high * 1,
          low: low * 1,
          close: close * 1,
        };
    });
    return cdata;
    // console.log(cdata);
};



const displayChart = async () => {
    const chartProperties = {
        width:1100,
        height:600,
        timeScale:{
            timeVisible:true,
            secondsVisible:true
        },
    };

    const domElement = document.getElementById("chartTest");
    const chart = LightweightCharts.createChart(domElement,chartProperties);
    const candleseries = chart.addCandlestickSeries();
    const klinedata = await getData();
    candleseries.setData(klinedata);
};

displayChart();
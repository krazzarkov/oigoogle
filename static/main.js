if (!window.dash_clientside) {
    window.dash_clientside = {};
}
window.dash_clientside.clientside = {
    trigger_hover: function(hoverData) {
        var date = new Date("2022-08-25T00:00:00");
        const userTimezoneOffset = date.getTimezoneOffset() * 60000;
        const ids = ["live-graph", "live-graph2", "live-graph3", "live-graph4", "binance_ratio", 'ftx_ratio', 'bybit_ratio', "live-graph5", "live-graph6", "live-graph7"]

        if (hoverData) {
            var x = hoverData.points[0].x
            x = Math.floor(new Date(x).getTime()) - userTimezoneOffset
            const arrayLength = ids.length
            for (var i = 0; i < arrayLength; i++) {
                id = ids[i]
                Plotly.Fx.hover(id, {yval: 0, xval : x})
            }
            
        }
        return window.dash_clientside.no_update
    }
}
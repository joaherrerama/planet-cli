class EvalScriptManager:
    def __init__(self):
        self.registry = {
            "ndvi_tiff": """
                //VERSION=3
                function setup() {
                    return {
                        input: ["B04", "B08"],
                        output: {
                            bands: 1,
                            sampleType: "FLOAT32"
                        }
                    };
                }

                function evaluatePixel(samples) {
                    return [index(samples.B08, samples.B04)]
                }
            """,
            "ndvi_png":"""
                //VERSION=3
                function setup() {
                    return {
                        input: ["B04", "B08", "dataMask"],
                        output: { bands: 4 }
                    };
                }

                const ramp = [
                    [-0.5, 0x0c0c0c],
                    [-0.2, 0xbfbfbf],
                    [-0.1, 0xdbdbdb],
                    [0, 0xeaeaea],
                    [0.025, 0xfff9cc],
                    [0.05, 0xede8b5],
                    [0.075, 0xddd89b],
                    [0.1, 0xccc682],
                    [0.125, 0xbcb76b],
                    [0.15, 0xafc160],
                    [0.175, 0xa3cc59],
                    [0.2, 0x91bf51],
                    [0.25, 0x7fb247],
                    [0.3, 0x70a33f],
                    [0.35, 0x609635],
                    [0.4, 0x4f892d],
                    [0.45, 0x3f7c23],
                    [0.5, 0x306d1c],
                    [0.55, 0x216011],
                    [0.6, 0x0f540a],
                    [1, 0x004400],
                ];

                const visualizer = new ColorRampVisualizer(ramp);

                function evaluatePixel(samples) {
                    let ndvi = index(samples.B08, samples.B04);
                    let imgVals = visualizer.process(ndvi);
                    return imgVals.concat(samples.dataMask)
                }

            """,
            "visual_tiff":"""
                //VERSION=3
                function setup(){
                    return{
                        input: ["B02", "B03", "B04", "dataMask"],
                        output: {bands: 4}
                    }
                }

                function evaluatePixel(sample){
                    // Set gain for visualisation
                    let gain = 2.5;
                    // Return RGB
                    return [sample.B04 * gain, sample.B03 * gain, sample.B02 * gain, sample.dataMask];
                }
            """,
            "visual_png":"""
                //VERSION=3
                function setup(){
                    return{
                        input: ["B02", "B03", "B04", "dataMask"],
                        output: {bands: 4}
                    }
                }

                function evaluatePixel(sample){
                    // Set gain for visualisation
                    let gain = 2.5;
                    // Return RGB
                    return [sample.B04 * gain, sample.B03 * gain, sample.B02 * gain, sample.dataMask];
                }
            """
        }

    def register(self, output_type: str, output_format: str, script):
        """Register Evalscript adding type and format as keys."""
        key = f"{output_format}_{output_type}"
        self.registry[key] = script

    def generate_script(self, output_type: str, output_format: str) -> str:
        """Get the eval script for a given type and format."""
        key = f"{output_type}_{output_format}"
        script = self.registry.get(key)

        if not script:
            raise ValueError(f"Unsupported type ({output_type}) or format ({output_format}).")

        return script
{
    "header": {
        "releaseVersion": "2025.1.0",
        "fileVersion": "2.0",
        "nodesVersions": {
            "CameraInit": "12.0",
            "FeatureExtraction": "1.3",
            "FeatureMatching": "2.0",
            "ImageMatching": "2.0",
            "SDMUniPS": "0.1",
            "SfMFilter": "1.0",
            "SfMTransfer": "2.1",
            "StructureFromMotion": "3.3"
        },
        "template": true
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                -400,
                200
            ],
            "inputs": {}
        },
        "FeatureExtraction_1": {
            "nodeType": "FeatureExtraction",
            "position": [
                0,
                0
            ],
            "inputs": {
                "input": "{SfMFilter_1.outputSfMData_selected}"
            }
        },
        "FeatureMatching_1": {
            "nodeType": "FeatureMatching",
            "position": [
                400,
                0
            ],
            "inputs": {
                "input": "{ImageMatching_1.input}",
                "featuresFolders": "{ImageMatching_1.featuresFolders}",
                "imagePairsList": "{ImageMatching_1.output}",
                "describerTypes": "{FeatureExtraction_1.describerTypes}",
                "maxIteration": 2048
            }
        },
        "ImageMatching_1": {
            "nodeType": "ImageMatching",
            "position": [
                200,
                0
            ],
            "inputs": {
                "input": "{FeatureExtraction_1.input}",
                "featuresFolders": [
                    "{FeatureExtraction_1.output}"
                ]
            }
        },
        "SDMUniPS_1": {
            "nodeType": "SDMUniPS",
            "position": [
                999,
                197
            ],
            "inputs": {
                "inputPath": "{SfMTransfer_1.output}"
            }
        },
        "SfMFilter_1": {
            "nodeType": "SfMFilter",
            "position": [
                -200,
                200
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}",
                "fileMatchingPattern": ".*/.*ambient.*"
            }
        },
        "SfMTransfer_1": {
            "nodeType": "SfMTransfer",
            "position": [
                800,
                200
            ],
            "inputs": {
                "input": "{SfMFilter_1.outputSfMData_unselected}",
                "reference": "{StructureFromMotion_1.output}",
                "method": "from_poseid"
            }
        },
        "StructureFromMotion_1": {
            "nodeType": "StructureFromMotion",
            "position": [
                600,
                0
            ],
            "inputs": {
                "input": "{FeatureMatching_1.input}",
                "featuresFolders": "{FeatureMatching_1.featuresFolders}",
                "matchesFolders": [
                    "{FeatureMatching_1.output}"
                ],
                "describerTypes": "{FeatureMatching_1.describerTypes}",
                "localizerEstimatorMaxIterations": 4096
            }
        }
    }
}
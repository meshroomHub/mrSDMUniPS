{
    "header": {
        "releaseVersion": "2026.1.0-develop",
        "fileVersion": "2.0",
        "nodesVersions": {
            "CameraInit": "12.0",
            "ConvertSfMFormat": "2.0",
            "ExportImages": "1.0",
            "FeatureExtraction": "1.3",
            "FeatureMatching": "2.0",
            "ImageDetectionPrompt": "0.1",
            "ImageMatching": "2.0",
            "ImageSegmentationBox": "0.2",
            "IntrinsicsTransforming": "1.0",
            "PreparePSImages": "0.1",
            "SDMUniPS": "0.1",
            "SfMFilter": "1.0",
            "SfMMerge": "3.0",
            "SfMTransfer": "2.1",
            "StructureFromMotion": "3.3"
        },
        "template": true
    },
    "graph": {
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                -514,
                25
            ],
            "inputs": {
                "viewpoints": [
                    {
                        "viewId": 18392806,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 22597331,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 27886994,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 35866863,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 37991353,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 45046704,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 46483756,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 49352094,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 51607453,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 58785120,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 71008480,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 82156418,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 101127754,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 105510237,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 107949523,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 114651635,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 124825925,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 131281711,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 143366393,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 150620114,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 159080748,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 166561941,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 169947199,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 188350033,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 191803517,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 193440496,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 202562048,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 213748540,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 221344558,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 230654901,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 242522156,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 245654866,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 263747403,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 268045740,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 274056866,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 290063407,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 294368368,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 296498799,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 333601928,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 346928856,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 348477838,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 359002502,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 359526207,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 363032799,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 372270148,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 379660747,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 401484586,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 404662567,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 414637762,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 421476900,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 441309136,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 451129545,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 466274352,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 470438736,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 479365573,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 482031387,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 527917066,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 530036176,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 549168715,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 561363921,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 573837412,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 575251431,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 590824713,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 597983371,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 603275409,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 606333086,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 607841902,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 632343073,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 635142171,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 638441731,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 650011470,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 653577525,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 670478907,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 676713881,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 676752860,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 684384224,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 685044870,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 689836665,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 698769314,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 703484388,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 720555147,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 722949903,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 724391872,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 728047417,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 734711716,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 760353772,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 772931502,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 779640579,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 806398743,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 817159462,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 826630179,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 847012145,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 850071872,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 857811777,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 866752254,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 880716599,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 894195201,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 918373613,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 933836383,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 942083532,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 957359222,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 988127937,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1008482054,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1025349667,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1037590527,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1054102314,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1117648485,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1119615653,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1120350066,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1122194621,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1138883351,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1142067395,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1145702118,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1146239200,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1150094112,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1151925282,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1158759684,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1159076613,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1166314440,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1181912085,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1189262197,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1190742362,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1195771961,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1200890573,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1210387121,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1211232973,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1217545507,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1218614646,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1220593393,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1232056817,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1257228130,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1260902765,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1273256422,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1277294090,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1292421366,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1324338631,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1329190787,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1330706607,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1335731440,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1345001307,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1358278147,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1364313191,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1394020361,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1397681599,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1404779261,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1410621243,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1445100358,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1445211081,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1446636068,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1450934622,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1454233853,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1465578813,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1466676763,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1499430044,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1516198623,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1520546120,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1522869074,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1534671300,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1540816127,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1546028268,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1551818606,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1554849062,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1556517662,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1565997382,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1573204955,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1584603937,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1592859634,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1593325965,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1643659853,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1663794613,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1664975320,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1669817723,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1673611805,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1690959382,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1709453297,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1722686713,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1725501305,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1730859543,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1743270832,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1751475630,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1756020502,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1756884209,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1768048400,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1773499941,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1773693710,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1775472207,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1775536186,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1788153968,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1793409962,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1802751555,
                        "poseId": 1573204955,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0099/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1806054099,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1810642476,
                        "poseId": 1775536186,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0051/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1816431124,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_right_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1824986713,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1831302289,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1832938241,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1840829266,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1845103965,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1857957102,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1858141107,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1862507912,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1868000131,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1868047233,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1868842137,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1890038128,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1892832198,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1904478592,
                        "poseId": 1037590527,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0080/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1904955935,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1905058884,
                        "poseId": 46483756,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0021/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1911837521,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1912351056,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1921408998,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1926618144,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1927812683,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/soft_left@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1931874440,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1932170399,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_left_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1935161628,
                        "poseId": 1663794613,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0092/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1940681211,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1943375354,
                        "poseId": 1892832198,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0069/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1957976567,
                        "poseId": 1840829266,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0039/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1973996611,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_right_top_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1975249382,
                        "poseId": 685044870,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0035/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1980174771,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/soft_top@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1980525531,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 1992780596,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2008133194,
                        "poseId": 1404779261,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0016/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2014959628,
                        "poseId": 479365573,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0010/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2016221179,
                        "poseId": 1220593393,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0005/hard_left_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2021344383,
                        "poseId": 1277294090,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0094/hard_right_bottom_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2022115526,
                        "poseId": 2022115526,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0097/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2034140848,
                        "poseId": 1534671300,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0001/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2053079158,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/flash@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2053821271,
                        "poseId": 2053821271,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0088/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2080255035,
                        "poseId": 1195771961,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0042/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2093998432,
                        "poseId": 2093998432,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0047/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2102839643,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/ambient@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2117978926,
                        "poseId": 676752860,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0075/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2131311503,
                        "poseId": 2102839643,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0062/hard_left_bottom_far@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2133493587,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/hard_left_top_close@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    },
                    {
                        "viewId": 2139486327,
                        "poseId": 1181912085,
                        "path": "/media/bbrument/T9/Skoltech3D/golden_snail/PS_0058/soft_right@best.png",
                        "intrinsicId": 1555508705,
                        "rigId": -1,
                        "subPoseId": -1,
                        "metadata": "{\"oiio:ColorSpace\": \"sRGB\"}"
                    }
                ],
                "intrinsics": [
                    {
                        "intrinsicId": 1555508705,
                        "initialFocalLength": -1.0,
                        "focalLength": 43.45584412271571,
                        "pixelRatio": 1.0,
                        "pixelRatioLocked": true,
                        "scaleLocked": false,
                        "offsetLocked": false,
                        "distortionLocked": false,
                        "type": "pinhole",
                        "distortionType": "radialk3",
                        "width": 2368,
                        "height": 1952,
                        "sensorWidth": 36.0,
                        "sensorHeight": 29.675675675675674,
                        "serialNumber": "",
                        "principalPoint": {
                            "x": 0.0,
                            "y": 0.0
                        },
                        "initializationMode": "unknown",
                        "distortionInitializationMode": "none",
                        "distortionParams": [
                            0.0,
                            0.0,
                            0.0
                        ],
                        "undistortionOffset": {
                            "x": 0.0,
                            "y": 0.0
                        },
                        "undistortionParams": [],
                        "locked": false
                    }
                ],
                "groupCameraFallback": "global"
            }
        },
        "ConvertSfMFormat_1": {
            "nodeType": "ConvertSfMFormat",
            "position": [
                1738,
                88
            ],
            "inputs": {
                "input": "{ExportImages_1.outputSfMData}",
                "fileExt": "json"
            }
        },
        "ExportImages_1": {
            "nodeType": "ExportImages",
            "position": [
                1545,
                157
            ],
            "inputs": {
                "input": "{IntrinsicsTransforming_1.input}",
                "target": "{IntrinsicsTransforming_1.output}",
                "outputFileType": "png",
                "masksFolders": [
                    "{ImageSegmentationBox_1.output}"
                ]
            }
        },
        "FeatureExtraction_1": {
            "nodeType": "FeatureExtraction",
            "position": [
                387,
                6
            ],
            "inputs": {
                "input": "{SfMMerge_1.output}",
                "masksFolder": "{ImageSegmentationBox_1.output}",
                "forceCpuExtraction": false
            }
        },
        "FeatureMatching_1": {
            "nodeType": "FeatureMatching",
            "position": [
                770,
                4
            ],
            "inputs": {
                "input": "{ImageMatching_1.input}",
                "featuresFolders": "{ImageMatching_1.featuresFolders}",
                "imagePairsList": "{ImageMatching_1.output}",
                "describerTypes": "{FeatureExtraction_1.describerTypes}",
                "maxIteration": 2048
            }
        },
        "ImageDetectionPrompt_1": {
            "nodeType": "ImageDetectionPrompt",
            "position": [
                39,
                277
            ],
            "inputs": {
                "input": "{SfMFilter_1.outputSfMData_selected}",
                "prompt": "main",
                "synonyms": "",
                "forceDetection": true
            }
        },
        "ImageMatching_1": {
            "nodeType": "ImageMatching",
            "position": [
                570,
                4
            ],
            "inputs": {
                "input": "{FeatureExtraction_1.input}",
                "featuresFolders": [
                    "{FeatureExtraction_1.output}"
                ]
            }
        },
        "ImageSegmentationBox_1": {
            "nodeType": "ImageSegmentationBox",
            "position": [
                216,
                276
            ],
            "inputs": {
                "input": "{ImageDetectionPrompt_1.input}",
                "bboxFolder": "{ImageDetectionPrompt_1.output}",
                "extension": "png"
            }
        },
        "IntrinsicsTransforming_1": {
            "nodeType": "IntrinsicsTransforming",
            "position": [
                1362,
                160
            ],
            "inputs": {
                "input": "{SfMTransfer_1.output}"
            }
        },
        "PreparePSImages_1": {
            "nodeType": "PreparePSImages",
            "position": [
                1802,
                203
            ],
            "inputs": {
                "inputPath": "{ExportImages_1.outputSfMData}",
                "enableLandscapeRotation": false,
                "enableCropping": true
            }
        },
        "SDMUniPS_1": {
            "nodeType": "SDMUniPS",
            "position": [
                2015,
                142
            ],
            "inputs": {
                "inputSfmData": "{PreparePSImages_1.outputSfmData}",
                "inputDataFolder": "{PreparePSImages_1.outputDataFolder}",
                "maxImageNum": 15,
                "viewExt": "{PreparePSImages_1.dataFolderSuffix}"
            }
        },
        "SfMFilter_1": {
            "nodeType": "SfMFilter",
            "position": [
                -136,
                152
            ],
            "inputs": {
                "inputFile": "{SfMFilter_2.outputSfMData_selected}",
                "fileMatchingPattern": ".*/ambient.*"
            }
        },
        "SfMFilter_2": {
            "nodeType": "SfMFilter",
            "position": [
                -325.0,
                19.0
            ],
            "inputs": {
                "inputFile": "{CameraInit_1.output}",
                "fileMatchingPattern": "PS_.*/.*"
            }
        },
        "SfMMerge_1": {
            "nodeType": "SfMMerge",
            "position": [
                194,
                7
            ],
            "inputs": {
                "inputs": [
                    "{SfMFilter_2.outputSfMData_unselected}",
                    "{SfMFilter_1.outputSfMData_selected}"
                ],
                "fileExt": "sfm"
            }
        },
        "SfMTransfer_1": {
            "nodeType": "SfMTransfer",
            "position": [
                1174,
                159
            ],
            "inputs": {
                "input": "{SfMFilter_1.inputFile}",
                "reference": "{StructureFromMotion_1.output}",
                "method": "from_poseid"
            }
        },
        "StructureFromMotion_1": {
            "nodeType": "StructureFromMotion",
            "position": [
                970,
                4
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
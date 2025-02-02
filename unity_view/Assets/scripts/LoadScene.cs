using UnityEngine;
using System.Collections.Generic;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

public class LoadScene : MonoBehaviour
{
    [System.Serializable]
    public class AssetInfo
    {
        public string stageName;
        public string filePath;
        public Vector3 position;
    }

    public string manifestPath = "../../Assets/manifest.yaml";

    void Start()
    {
        LoadAssetsFromManifest();
    }

    void LoadAssetsFromManifest()
    {
        if (!File.Exists(manifestPath))
        {
            Debug.LogError("Manifest file not found: " + manifestPath);
            return;
        }

        string yamlContent = File.ReadAllText(manifestPath);
        var deserializer = new DeserializerBuilder()
            .WithNamingConvention(CamelCaseNamingConvention.Instance)
            .Build();

        var assets = deserializer.Deserialize<List<AssetInfo>>(yamlContent);

        foreach (var asset in assets)
        {
            string assetPath = Path.Combine(Application.dataPath, asset.filePath);
            if (File.Exists(assetPath))
            {
                GameObject assetPrefab = LoadAsset(assetPath);
                if (assetPrefab != null)
                {
                    Instantiate(assetPrefab, asset.position, Quaternion.identity);
                }
            }
            else
            {
                Debug.LogError("Asset file not found: " + assetPath);
            }
        }
    }

    GameObject LoadAsset(string assetPath)
    {
        // Implement the logic to load the asset from the file path
        // This is a placeholder implementation, you need to adjust it based on your asset loading method
        // For example, you might use AssetBundle or Resources.Load
        return null;
    }
}
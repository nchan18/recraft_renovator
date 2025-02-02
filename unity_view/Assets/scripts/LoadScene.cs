using System.Collections.Generic;
using System.IO;
using UnityEngine;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;
using Siccity.GLTFUtility; // GLTFUtility namespace

public class GLBManifestImporter : MonoBehaviour
{
    public static string currentDirectory = Directory.GetCurrentDirectory();
    public string manifestFilePath = Path.Combine(currentDirectory, "../Assets/manifest.yaml");

    [System.Serializable]
    public class AssetInfo
    {
        public string stageName;
        public string filePath;
        public Vector3 position;
        public Vector3 rotation;
    }

    void Start()
    {
        LoadManifest();
    }

    void LoadManifest()
    {
        string filePath = Path.Combine(Application.streamingAssetsPath, manifestFilePath);
        if (File.Exists(filePath))
        {
            string yamlContent = File.ReadAllText(filePath);

            var deserializer = new DeserializerBuilder()
                .WithNamingConvention(CamelCaseNamingConvention.Instance)
                .Build();

            var assets = deserializer.Deserialize<Dictionary<string, AssetInfo>>(yamlContent);

            foreach (var assetEntry in assets)
            {
                ImportGLB(assetEntry.Value);
            }
        }
        else
        {
            Debug.LogError("Manifest file not found: " + filePath);
        }
    }

    void ImportGLB(AssetInfo assetInfo)
    {
        string glbPath = Path.Combine(Application.streamingAssetsPath, assetInfo.filePath);
        if (File.Exists(glbPath))
        {
            // Load the GLB file using GLTFUtility
            GameObject glbObject = Importer.LoadFromFile(glbPath);

            if (glbObject != null)
            {
                // Set the position and rotation
                glbObject.transform.position = assetInfo.position;
                glbObject.transform.rotation = Quaternion.Euler(assetInfo.rotation);
                glbObject.name = assetInfo.stageName;
            }
            else
            {
                Debug.LogError("Failed to load GLB file: " + glbPath);
            }
        }
        else
        {
            Debug.LogError("GLB file not found: " + glbPath);
        }
    }
}
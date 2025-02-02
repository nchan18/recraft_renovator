using UnityEngine;
using UnityEngine.UI;
using System.IO;

public class AddItem : MonoBehaviour
{
    public Button addAssetButton;
    public InputField filePathInputField;

    void Start()
    {
        addAssetButton.onClick.AddListener(OnAddAssetButtonClick);
    }

    void OnAddAssetButtonClick()
    {
        string filePath = filePathInputField.text;
        if (File.Exists(filePath) && Path.GetExtension(filePath).ToLower() == ".glb")
        {
            // Load the GLB asset
            LoadGLBAsset(filePath);
        }
        else
        {
            Debug.LogError("Invalid file path or file type. Please enter a valid .glb file path.");
        }
    }

    void LoadGLBAsset(string filePath)
    {
        // Implement the logic to load the GLB asset
        Debug.Log("Loading GLB asset from: " + filePath);
        // Example: Use a GLB loader library to load the asset
    }
}
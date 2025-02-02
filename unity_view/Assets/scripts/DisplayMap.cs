using UnityEngine;
using UnityEngine.UI;

public class DisplayMap : MonoBehaviour
{
    public RawImage mapImage;
    public Image cameraMarker;
    public Camera camera1;

    void Start()
    {
        // Set the map image (assuming the map is located in the Assets folder)
        Texture2D mapTexture = Resources.Load<Texture2D>("map");
        mapImage.texture = mapTexture;
    }

    void Update()
    {
        // Update the camera marker position based on camera1's location
        Vector2 mapPosition = GetMapPosition(camera1.transform.position);
        cameraMarker.rectTransform.anchoredPosition = mapPosition;
    }

    Vector2 GetMapPosition(Vector3 worldPosition)
    {
        // Convert the world position to map position
        // This is a placeholder implementation, you need to adjust it based on your map and world coordinates
        float mapWidth = mapImage.rectTransform.rect.width;
        float mapHeight = mapImage.rectTransform.rect.height;
        float x = (worldPosition.x / 100.0f) * mapWidth;
        float y = (worldPosition.z / 100.0f) * mapHeight;
        return new Vector2(x, y);
    }
}
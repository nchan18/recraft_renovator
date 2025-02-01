using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    public int Speed = 50;

    void Update()
    {
        float xAxisValue = Input.GetAxis("Horizontal") * Speed * Time.deltaTime;
        float zAxisValue = Input.GetAxis("Vertical") * Speed * Time.deltaTime;
        float yValue = 0.0f;

        if (Input.GetKey(KeyCode.Q))
        {
            yValue = -Speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.E))
        {
            yValue = Speed * Time.deltaTime;
        }

        transform.position = new Vector3(transform.position.x + xAxisValue, transform.position.y + yValue, transform.position.z + zAxisValue);
    }
}
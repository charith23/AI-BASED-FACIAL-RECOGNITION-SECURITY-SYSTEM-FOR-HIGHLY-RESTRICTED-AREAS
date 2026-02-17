import cv2

def test(src):
    cap = cv2.VideoCapture(src, cv2.CAP_V4L2)
    if not cap.isOpened():
        return False, None

    ret, frame = cap.read()
    cap.release()
    if ret and frame is not None:
        return True, frame.shape
    return False, None


def main():
    print("Scanning camera indexes 0 to 10...")
    for i in range(0, 11):
        ok, shape = test(i)
        if ok:
            print(f"? Camera index {i} works! frame shape = {shape}")
        else:
            print(f"? Camera index {i} failed")

if __name__ == "__main__":
    main()

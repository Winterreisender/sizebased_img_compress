import mozjpeg_lossless_optimization as mozjpeg


#%%
lossless_bytes = mozjpeg.optimize(img_bytes)
print(len(lossless_bytes))

#%%
img = cv2.imread('example.png', flags= cv2.IMREAD_UNCHANGED)

img_bytes = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80] )[1]


print(img_bytes, img_bytes.size)
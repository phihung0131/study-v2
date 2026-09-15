# Ôn tập phỏng vấn: Two Pointers + Sliding Window

> Nhóm này rất hay gặp vì nó test khả năng nhận diện pattern: khi nào dùng 2 con trỏ chạy về nhau, khi nào dùng cửa sổ trượt (mở rộng/thu hẹp), khi nào chỉ cần theo dõi 1 biến chạy qua mảng.

---

## 1. Best Time to Buy and Sell Stock

### Đề bài
Cho mảng `prices`, `prices[i]` là giá cổ phiếu ngày thứ i. Bạn chỉ được **mua 1 lần, bán 1 lần** (mua trước bán sau). Tìm lợi nhuận lớn nhất có thể đạt được. Nếu không có lãi, trả về 0.

**Ví dụ:** `prices = [7,1,5,3,6,4]` → `5` (mua ngày giá 1, bán ngày giá 6)

### Hướng làm
- **Brute force (O(n²)):** với mỗi cặp (i, j) với i < j, tính `prices[j] - prices[i]`, lấy max. Quá chậm.
- **Tối ưu (O(n)) — "one-pass" giữ min:** duyệt qua mảng 1 lần, giữ biến `min_price` = giá thấp nhất đã gặp **tính đến hiện tại**. Tại mỗi bước, tính lợi nhuận nếu bán ở giá hiện tại (`price - min_price`), cập nhật `max_profit` nếu lớn hơn.

```python
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```

Đây thực ra là dạng "two pointers cùng chiều": một con trỏ ngầm định là `min_price` (giữ vị trí thấp nhất từ trái), con trỏ còn lại là `price` hiện tại quét qua.

### Cách trình bày khi phỏng vấn
1. Nhấn mạnh ràng buộc quan trọng: **phải mua trước bán sau** (không được bán trước mua) — đây là điểm dễ bị hiểu sai đề.
2. Nêu insight cốt lõi: "Để lợi nhuận tại ngày j lớn nhất, mình cần mua ở giá **thấp nhất trong các ngày trước j**." → không cần thử mọi cặp, chỉ cần nhớ min chạy dần.
3. Dry-run ví dụ: `[7,1,5,3,6,4]` → chỉ ra từng bước `min_price` và `max_profit` cập nhật ra sao.
4. Độ phức tạp: Time O(n), Space O(1).
5. Follow-up hay gặp: "Nếu được mua bán nhiều lần thì sao?" → đó là bài khác (Buy/Sell Stock II), dùng greedy cộng dồn mọi đoạn tăng giá — nên biết để trả lời nhanh nếu bị hỏi thêm.

---

## 2. Container With Most Water

### Đề bài
Cho mảng `height`, `height[i]` là chiều cao vạch thứ i. Chọn 2 vạch `i, j` sao cho cùng với trục hoành tạo thành 1 cái "thùng chứa nước", diện tích chứa = `min(height[i], height[j]) * (j - i)`. Tìm diện tích lớn nhất.

**Ví dụ:** `height = [1,8,6,2,5,4,8,3,7]` → `49`

### Hướng làm
- **Brute force (O(n²)):** thử mọi cặp (i, j), tính diện tích, lấy max.
- **Tối ưu (O(n)) — Two Pointers từ 2 đầu:**
  - Đặt `left = 0`, `right = n - 1`.
  - Tính diện tích hiện tại = `min(height[left], height[right]) * (right - left)`, cập nhật max.
  - **Insight quan trọng:** vì diện tích bị giới hạn bởi cạnh **thấp hơn**, nên di chuyển con trỏ ở cạnh thấp hơn vào trong (vì giữ nguyên nó chỉ làm khoảng cách giảm mà chiều cao không tăng — chắc chắn không tốt hơn). Di chuyển con trỏ cao hơn thì có cơ hội tìm được vạch cao hơn nữa.
  - Lặp đến khi `left == right`.

```python
def maxArea(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])
        best = max(best, h * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
```

### Cách trình bày khi phỏng vấn
1. Vẽ hình minh họa (nếu có bảng/giấy) — bài này rất trực quan, vẽ ra sẽ giúp cả bạn và interviewer dễ theo dõi.
2. Giải thích **tại sao** brute force lãng phí: "Không cần thử mọi cặp — nếu cố định cạnh thấp hơn và không di chuyển nó, mọi cặp j còn lại chắc chắn cho diện tích ≤ diện tích hiện tại vì khoảng cách bị thu hẹp mà chiều cao vẫn bị giới hạn bởi cạnh thấp đó."
3. Đây là phần **chứng minh greedy đúng** — nói rõ phần này thường gây ấn tượng mạnh, vì nhiều người chỉ code đúng mà không giải thích được tại sao 2 pointer lại work.
4. Độ phức tạp: Time O(n), Space O(1).

---

## 3. Longest Substring Without Repeating Characters

### Đề bài
Cho chuỗi `s`, tìm độ dài của **chuỗi con liên tiếp dài nhất** không chứa ký tự lặp lại.

**Ví dụ:** `s = "abcabcbb"` → `3` (chuỗi con `"abc"`)

### Hướng làm
Đây là bài kinh điển của **Sliding Window (cửa sổ trượt biến đổi kích thước)**.

- **Brute force (O(n³)):** thử mọi chuỗi con, kiểm tra có ký tự lặp không → quá chậm.
- **Tối ưu (O(n)) — Sliding Window + Hash Set/Map:**
  - Dùng 2 con trỏ `left`, `right` tạo thành 1 "cửa sổ" `[left, right]`.
  - Mở rộng `right` sang phải, thêm ký tự vào set.
  - Nếu ký tự tại `right` đã có trong cửa sổ → thu hẹp từ bên trái (`left` tăng dần, loại ký tự ra khỏi set) cho đến khi hết trùng.
  - Theo dõi độ dài cửa sổ lớn nhất qua từng bước.

```python
def lengthOfLongestSubstring(s):
    seen = set()
    left = 0
    best = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        best = max(best, right - left + 1)
    return best
```

**Biến thể nhanh hơn (dùng hash map lưu vị trí):** thay vì thu hẹp từng bước 1, có thể "nhảy" `left` thẳng đến vị trí sau ký tự trùng gần nhất:

```python
def lengthOfLongestSubstring(s):
    last_seen = {}  # char -> index gần nhất
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

### Cách trình bày khi phỏng vấn
1. Nhận diện ngay đây là dạng "tìm đoạn con thỏa điều kiện, độ dài thay đổi" → đây là **tín hiệu kinh điển của Sliding Window**. Nói thẳng điều này với interviewer để họ thấy bạn nhận diện pattern nhanh.
2. Giải thích invariant của thuật toán: "Cửa sổ `[left, right]` luôn đảm bảo không có ký tự trùng — mỗi khi vi phạm, chỉ cần co `left` lại, không cần bắt đầu lại từ đầu."
3. Phân tích lý do độ phức tạp là O(n) dù có vòng `while` lồng trong `for`: **mỗi ký tự chỉ được thêm và xóa khỏi cửa sổ tối đa 1 lần** → tổng số thao tác vẫn là O(n) (amortized), không phải O(n²).
4. Nếu còn thời gian, chủ động trình bày thêm bản tối ưu bằng hash map lưu vị trí (nhảy `left` trực tiếp) — thể hiện bạn biết cách tối ưu hằng số.

---

## 4. Maximum Subarray (Kadane's Algorithm)

### Đề bài
Cho mảng số nguyên `nums` (có thể có số âm), tìm **tổng lớn nhất** của một dãy con liên tiếp (subarray) không rỗng.

**Ví dụ:** `nums = [-2,1,-3,4,-1,2,1,-5,4]` → `6` (dãy con `[4,-1,2,1]`)

### Hướng làm
- **Brute force (O(n²)):** thử mọi cặp điểm đầu-cuối, tính tổng → chậm.
- **Kadane's Algorithm (O(n)):** dùng quy hoạch động (DP) đơn giản với 1 biến chạy.
  - Ý tưởng: tại mỗi vị trí i, quyết định "có nên **tiếp tục cộng dồn** dãy con hiện tại, hay **bỏ hết và bắt đầu lại** từ `nums[i]`?"
  - Nếu tổng dãy con hiện tại (`current_sum`) bị âm → nó chỉ làm giảm giá trị dãy con tiếp theo → **bỏ, bắt đầu lại từ `nums[i]`**.
  - Ngược lại → cộng dồn tiếp.

```python
def maxSubArray(nums):
    current_sum = nums[0]
    best_sum = nums[0]
    for x in nums[1:]:
        current_sum = max(x, current_sum + x)
        best_sum = max(best_sum, current_sum)
    return best_sum
```

### Cách trình bày khi phỏng vấn
1. Đây thực chất là bài **Dynamic Programming** trá hình chứ không hẳn two-pointer — nên nói rõ: "Bài này thuộc dạng DP 1 chiều, nhưng vì chỉ cần trạng thái ngay trước đó nên có thể tối ưu về O(1) space, giống cách tiếp cận của Sliding Window."
2. Giải thích rõ **công thức truy hồi**: `dp[i] = max(nums[i], dp[i-1] + nums[i])` — nghĩa là dãy con tốt nhất kết thúc tại i, hoặc là chỉ mình `nums[i]`, hoặc là nối tiếp dãy con tốt nhất kết thúc tại i-1.
3. Nhấn mạnh: `best_sum` (đáp án cuối) khác với `current_sum` (trạng thái DP) — nhiều người nhầm lẫn 2 biến này khi code, cần phân biệt rõ khi giải thích.
4. Follow-up hay gặp: "Nếu cần trả về **chính dãy con đó** (không chỉ tổng) thì sao?" → giữ thêm biến `start`, `end` đánh dấu vị trí khi reset.
5. Follow-up khác: "Giải bằng Divide & Conquer được không?" → có, O(n log n), nhưng Kadane's O(n) vẫn tối ưu hơn — nên biết để trả lời nếu bị hỏi.

---

## 5. 3Sum (nếu còn thời gian)

### Đề bài
Cho mảng số nguyên `nums`, tìm **tất cả bộ ba** `(nums[i], nums[j], nums[k])` sao cho `i ≠ j ≠ k` và tổng bằng 0. Kết quả không được chứa bộ ba trùng lặp.

**Ví dụ:** `nums = [-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`

### Hướng làm
Đây là bài mở rộng của Two Sum, kết hợp **Sort + Two Pointers**.

- **Brute force (O(n³)):** thử mọi bộ ba → quá chậm và khó loại trùng.
- **Tối ưu (O(n²)):**
  1. **Sort** mảng trước (O(n log n)) — giúp dễ loại trùng và dùng 2 pointer.
  2. Duyệt `i` từ 0 đến n-3, cố định `nums[i]` làm số đầu tiên.
     - Bỏ qua nếu `nums[i] == nums[i-1]` (tránh trùng bộ ba).
     - Nếu `nums[i] > 0`, dừng luôn (vì mảng đã sort, không thể có tổng = 0 với số dương ở đầu).
  3. Với phần còn lại `[i+1, n-1]`, dùng **2 pointer** `left = i+1`, `right = n-1` để tìm cặp có tổng = `-nums[i]` (giống bài Two Sum trên mảng đã sort).
     - Nếu tổng 3 số = 0 → lưu kết quả, di chuyển cả `left` và `right`, đồng thời bỏ qua các giá trị trùng liền kề.
     - Nếu tổng < 0 → tăng `left` (cần số lớn hơn).
     - Nếu tổng > 0 → giảm `right` (cần số nhỏ hơn).

```python
def threeSum(nums):
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result
```

### Cách trình bày khi phỏng vấn
1. Liên hệ ngay với Two Sum: "Bài này về bản chất là Two Sum, nhưng thêm 1 lớp lặp bên ngoài để cố định số đầu tiên, rồi giải Two Sum cho phần còn lại bằng 2 pointer thay vì hash map — vì mảng đã sort nên 2 pointer hiệu quả hơn và giúp xử lý trùng lặp dễ hơn."
2. Nhấn mạnh **lý do sort trước**: (1) giúp 2 pointer hoạt động đúng logic tăng/giảm, (2) giúp **loại bộ ba trùng lặp** dễ dàng bằng cách so sánh phần tử liền kề — đây là phần code hay bị thiếu/sai nhất, nên nói kỹ.
3. Giải thích early-exit `if nums[i] > 0: break` — thể hiện bạn tận dụng được tính chất mảng đã sort để cắt nhánh sớm, không chỉ chạy hết vòng lặp.
4. Độ phức tạp: Time O(n²) (vòng ngoài O(n) × two-pointer bên trong O(n)), Space O(1) hoặc O(n) tùy có tính chỗ chứa kết quả sort hay không.
5. Đây là bài "phân loại" ứng viên khá rõ trong phỏng vấn — nếu code sạch, xử lý trùng lặp đúng, và giải thích được lý do sort, sẽ ghi điểm tốt.

---

## Bí quyết chung khi phỏng vấn nhóm Two Pointers / Sliding Window

- **Dấu hiệu nhận biết dùng Two Pointers:** mảng đã sort (hoặc có thể sort), cần tìm cặp/bộ thỏa điều kiện tổng, hoặc so sánh từ 2 đầu vào giữa (palindrome, container...).
- **Dấu hiệu nhận biết dùng Sliding Window:** cần tìm đoạn con liên tiếp (subarray/substring) thỏa điều kiện, độ dài đoạn có thể thay đổi, và điều kiện "đơn điệu" (mở rộng cửa sổ làm điều kiện dễ vi phạm hơn, thu hẹp làm dễ thỏa hơn).
- Luôn **giải thích invariant** (bất biến) của cửa sổ/con trỏ đang giữ — đây là phần interviewer đánh giá cao nhất, vì nó chứng minh thuật toán đúng chứ không phải "may mắn code chạy".
- Luôn phân tích rõ vì sao độ phức tạp là O(n) dù nhìn có vẻ có vòng lặp lồng nhau (amortized analysis) — pattern này lặp lại ở cả bài 3 và 5.
- Nhắc lại: nêu brute force trước → chỉ ra điểm nghẽn (bottleneck) → dẫn dắt tự nhiên đến giải pháp tối ưu, thay vì nhảy thẳng vào code tối ưu mà không giải thích.

Chúc bạn phỏng vấn thuận lợi! 🍀

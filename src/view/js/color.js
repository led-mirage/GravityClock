// "#ffffff" や "#fff" を RGB に変換する関数
function hexToRgb(hex) {
    if (typeof hex !== 'string') return null;

    // 先頭の # を削除
    let value = hex.trim().toLowerCase();
    if (value.startsWith('#')) {
        value = value.slice(1);
    }

    // 3桁表記(#fff) を 6桁表記(ff -> fff -> ffffff) に変換
    if (value.length === 3) {
        value = value.split('').map(ch => ch + ch).join('');
    }

    // 6桁でなければ無効
    if (value.length !== 6) return null;

    // 16進数として妥当かチェック
    if (!/^[0-9a-f]{6}$/.test(value)) return null;

    const r = parseInt(value.slice(0, 2), 16);
    const g = parseInt(value.slice(2, 4), 16);
    const b = parseInt(value.slice(4, 6), 16);

    return { r: r, g: g, b: b };
}

// "#ffffff" や "#fff" を HSL に変換する関数
function hexToHsl(hex) {
    const rgb = hexToRgb(hex);
    return rgbToHsl(rgb);
}

// RGB値(0〜255) を HSL値に変換する関数
function rgbToHsl(rgb) {
    // 0〜1 に正規化
    const R = rgb.r / 255;
    const G = rgb.g / 255;
    const B = rgb.b / 255;

    const max = Math.max(R, G, B);
    const min = Math.min(R, G, B);
    const diff = max - min;

    // Lightness
    const l = (max + min) / 2;

    let h = 0;
    let s = 0;

    if (diff !== 0) {
        // Saturation
        s = diff / (1 - Math.abs(2 * l - 1));

        // Hue
        switch (max) {
            case R:
                h = ((G - B) / diff) % 6;
                break;
            case G:
                h = (B - R) / diff + 2;
                break;
            case B:
                h = (R - G) / diff + 4;
                break;
        }
        h *= 60;
        if (h < 0) h += 360;
    }

    return {
        h: Math.round(h),
        s: Math.round(s * 100),
        l: Math.round(l * 100)
    };
}

// HSL値を"#ffffff"に変換する関数
function hslToHex(h, s, l) {
    s /= 100; l /= 100;
    const c = (1 - Math.abs(2 * l - 1)) * s;
    const hp = h / 60;
    const x = c * (1 - Math.abs((hp % 2) - 1));
    let r = 0, g = 0, b = 0;

    if (0 <= hp && hp < 1) [r, g, b] = [c, x, 0];
    else if (1 <= hp && hp < 2) [r, g, b] = [x, c, 0];
    else if (2 <= hp && hp < 3) [r, g, b] = [0, c, x];
    else if (3 <= hp && hp < 4) [r, g, b] = [0, x, c];
    else if (4 <= hp && hp < 5) [r, g, b] = [x, 0, c];
    else if (5 <= hp && hp < 6) [r, g, b] = [c, 0, x];

    const m = l - c / 2;
    const to255 = v => Math.round((v + m) * 255);
    const hex = n => n.toString(16).padStart(2, "0");

    return "#" + hex(to255(r)) + hex(to255(g)) + hex(to255(b));
}

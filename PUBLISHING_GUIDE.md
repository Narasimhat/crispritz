# Digital Publishing Guide for "The Lighthouse Within"

## Overview

Your book has been successfully converted to EPUB format, which is compatible with:
- **Amazon Kindle Direct Publishing (KDP)**
- **Apple Books**
- **Google Play Books**
- **Kobo**
- **Barnes & Noble Nook**

## Files Created

- `lighthouse_within.epub` - Your ebook file (15 KB)
- `lighthouse_within.tex` - Original LaTeX source
- `latex_to_epub.py` - Conversion script (for future updates)

## Publishing on Amazon Kindle (KDP)

### Step 1: Create a KDP Account
1. Go to https://kdp.amazon.com
2. Sign in with your Amazon account or create a new one
3. Complete your account information

### Step 2: Create a New Kindle eBook
1. Click "Create" → "Kindle eBook"
2. Fill in the book details:
   - **Title**: The Lighthouse Within
   - **Subtitle**: A New Year Gift for Dreamers
   - **Author**: The Lighthouse Within (or your name)
   - **Description**: Write a compelling description
   - **Keywords**: personal development, morning routine, self-help, motivation, productivity
   - **Categories**: Choose 2 relevant categories (e.g., Self-Help / Personal Transformation)

### Step 3: Upload Your Content
1. In the "Manuscript" section:
   - Upload `lighthouse_within.epub`
   - KDP will automatically convert it to Kindle format
2. Preview your book using the online previewer
3. Check all chapters display correctly

### Step 4: Set Pricing
1. **Rights**: Worldwide rights (unless you have restrictions)
2. **Pricing**:
   - Recommended: $2.99 - $9.99 (earns 70% royalty)
   - Under $2.99 earns 35% royalty
3. **Kindle Unlimited**: Decide if you want to enroll (gives exclusivity to Amazon)

### Step 5: Publish
1. Review all information
2. Click "Publish Your Kindle eBook"
3. Your book will be live within 24-72 hours

## Publishing on Apple Books

### Step 1: Get Apple Books Tools
1. You need a Mac computer with macOS
2. Download "Apple Books for Authors" app from App Store
3. Or use the web-based Apple Books Partner portal

### Step 2: Create an Account
1. Go to https://books.apple.com/us/author
2. Sign in with your Apple ID
3. Agree to the terms and conditions
4. Provide tax information

### Step 3: Upload Your Book
1. Open Apple Books for Authors or the web portal
2. Click "Add a Book"
3. Upload `lighthouse_within.epub`
4. Fill in metadata:
   - Title, Author, Description
   - Cover image (you'll need to create one - see below)
   - Categories and keywords
   - ISBN (optional for self-publishing)

### Step 4: Set Pricing
1. Choose your territories (countries)
2. Set price (Apple Books takes 30% commission)
3. Recommended: $2.99 - $9.99

### Step 5: Submit for Review
1. Review all details
2. Submit for approval
3. Apple will review (typically 1-3 business days)
4. Once approved, your book goes live

## Cover Image Requirements

You'll need a cover image for digital publishing:

### Specifications:
- **Minimum size**: 1600 x 2400 pixels (2:3 ratio)
- **Recommended size**: 2560 x 1600 pixels or larger
- **Format**: JPEG or PNG
- **Color**: RGB
- **File size**: Under 5 MB

### Design Tips:
1. Keep text large and readable (will appear as thumbnail)
2. Use high contrast colors
3. Include title and author name
4. Simple, bold design works best for digital

### Free Design Tools:
- Canva (https://canva.com) - has ebook cover templates
- GIMP (free Photoshop alternative)
- Photopea (browser-based, Photoshop-like)

## Publishing on Other Platforms

### Google Play Books
1. Go to https://play.google.com/books/publish
2. Upload `lighthouse_within.epub`
3. Similar process to KDP

### Draft2Digital (Aggregator)
- Publishes to multiple retailers at once
- Takes 10% commission but handles distribution
- URL: https://draft2digital.com

### Smashwords (Aggregator)
- Free distribution to multiple retailers
- URL: https://smashwords.com

## Pricing Strategy Recommendations

### Free Launch Strategy:
1. Price at $0.99 for first week (builds reviews)
2. Increase to $2.99-$4.99 after launch
3. Run promotions periodically

### Standard Pricing:
- **$2.99** - Good entry price, 70% royalty on Amazon
- **$4.99** - Middle tier, perceived value
- **$9.99** - Premium self-help book pricing

## Marketing Checklist

- [ ] Create social media accounts for the book
- [ ] Build an email list
- [ ] Ask early readers for reviews
- [ ] Create a book website or landing page
- [ ] Join relevant Facebook/Reddit groups
- [ ] Consider Amazon ads (after launch)
- [ ] Reach out to book bloggers
- [ ] Create a book trailer (video)

## Legal Considerations

1. **Copyright**: Your book is automatically copyrighted when created
2. **ISBN**: Optional for ebook-only publishing
   - Amazon provides free ASIN (Amazon Standard Identification Number)
   - Apple Books can use Apple-assigned ISBN
3. **Tax**: Provide tax information to retailers
4. **Content**: Ensure you have rights to all content

## Quality Checklist Before Publishing

- [ ] Proofread the EPUB in a reader app
- [ ] Check chapter headings display correctly
- [ ] Verify reflection boxes format properly
- [ ] Test on multiple devices (phone, tablet, e-reader)
- [ ] Ensure all links work (if any)
- [ ] Check table of contents is correct

## Testing Your EPUB

### On Desktop:
- **Calibre** (free): Download from https://calibre-ebook.com
- **Adobe Digital Editions**: Free from Adobe

### On Mobile:
- **Apple Books** (iOS)
- **Google Play Books** (Android)
- **Kindle app**: Transfer via email or USB

### Online Validators:
- **EPUB Validator**: http://validator.idpf.org
- Upload your EPUB to check for errors

## Updating Your Book

If you need to make changes:

1. Edit the original LaTeX file (`lighthouse_within.tex`)
2. Run the conversion script:
   ```bash
   python3 latex_to_epub.py
   ```
3. Test the new EPUB file
4. Upload the updated file to KDP/Apple Books
5. Changes go live within 24-72 hours

## Support and Resources

### Communities:
- **r/selfpublish** (Reddit)
- **KBoards / Kboards Writers**
- **20Booksto50K Facebook Group**

### Learning Resources:
- Amazon KDP Help: https://kdp.amazon.com/help
- Apple Books Resources: https://authors.apple.com/support
- The Creative Penn (blog/podcast): https://thecreativepenn.com

## Troubleshooting

### EPUB Not Accepted:
- Validate using http://validator.idpf.org
- Check file size (should be under 50 MB)
- Ensure no special characters in filename

### Formatting Issues:
- Test in multiple reading apps
- Italics and bold should work
- Reflection boxes appear as styled sections

### Cover Not Displaying:
- Check image dimensions (min 1600x2400)
- Ensure RGB color mode (not CMYK)
- File should be under 5 MB

## Next Steps

1. **Create a cover image** using Canva or hire a designer
2. **Set up your KDP account**
3. **Upload your EPUB**
4. **Set your price**
5. **Publish!**

## Congratulations!

Your book is ready for digital publication. The EPUB file is professionally formatted and compatible with all major ebook retailers.

Good luck with your launch! 🎉

---

**Questions?** The conversion script can be modified if you need any formatting changes. Just edit `lighthouse_within.tex` and run the script again.

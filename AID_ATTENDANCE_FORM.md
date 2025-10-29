# Aid & Attendance Form

## Overview
The Aid & Attendance Form is a comprehensive intake form designed specifically for veterans and surviving spouses seeking Aid & Attendance benefits. This form streamlines the evaluation process by collecting all necessary information upfront.

## Features

### Form Sections
1. **Veteran Information**
   - Personal details (name, SSN, DOB, contact info)
   - Required fields for identification

2. **Contact Person Information**
   - Optional section for caregivers or family members
   - Relationship tracking
   - Separate contact details

3. **Medical Information**
   - Primary and secondary diagnoses
   - Current medications
   - Physician information
   - Last examination date

4. **Activities of Daily Living (ADL) Assessment**
   - Bathing/Showering
   - Dressing/Undressing
   - Eating/Feeding
   - Toileting
   - Walking/Mobility
   - Transferring (bed to chair)
   - Continence Control

5. **Care Requirements**
   - Supervision level needed
   - Hours of assistance required
   - Current caregiver information

6. **Additional Information**
   - Free-form text for additional details
   - Rush service option (+$500 for 36-48 hours)

### Technical Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Form Validation**: Required field validation with user-friendly error messages
- **File Upload Integration**: Supports document uploads after form submission
- **HIPAA Compliant**: Secure handling of medical information
- **Progress Indication**: Clear section organization with visual hierarchy

## Pricing Integration
- **Standard Service**: $2,000 (7-10 business days)
- **Rush Service**: +$500 (36-48 hours delivery)
- **Pricing Display**: Prominent pricing information at the top of the form

## User Experience
- **Multi-step Layout**: Organized into logical sections
- **Visual Indicators**: Icons and color coding for different sections
- **Success State**: Comprehensive confirmation with next steps
- **File Upload**: Post-submission document upload capability

## Integration Points

### Frontend Routes
- `/aid-attendance-form` - Main form page
- Accessible from:
  - Services page (special "Start Form" button)
  - Service detail page for Aid & Attendance
  - Footer navigation

### Backend Integration
- Uses existing `/api/contact` endpoint
- Includes service type identification
- Supports file upload workflow

### Navigation Integration
- **Services Page**: Special form button alongside "View Details"
- **Service Detail Page**: Primary CTA for Aid & Attendance service
- **Footer**: Quick access link labeled "A&A Form"

## Form Validation
- Required fields marked with asterisks (*)
- Client-side validation for email format
- Phone number formatting
- Date validation
- Dropdown selections for standardized responses

## Accessibility Features
- Semantic HTML structure
- Proper form labels
- Keyboard navigation support
- Screen reader friendly
- High contrast design
- Clear visual hierarchy

## Mobile Optimization
- Responsive grid layout
- Touch-friendly form controls
- Optimized button sizes
- Readable text on small screens
- Proper viewport handling

## Security Considerations
- HTTPS transmission
- No sensitive data stored in localStorage
- Secure form submission
- HIPAA compliance messaging
- Privacy notice included

## Future Enhancements
- Form progress saving
- Multi-page form with progress indicator
- PDF generation of submitted form
- Email confirmation with form summary
- Integration with calendar scheduling
- Automated follow-up workflows

## Usage Analytics
The form includes data-testid attributes for tracking:
- Form submission rates
- Section completion rates
- Rush service selection
- File upload usage
- User journey analysis

## Support Information
- Clear next steps after submission
- Contact information for questions
- Expected timeline communication
- Document upload instructions
- Process explanation
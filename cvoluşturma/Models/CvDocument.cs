using System;
using System.ComponentModel.DataAnnotations;

namespace cvoluşturma.Models
{
    public class CvDocument
    {
        public int Id { get; set; }
        
        [Required]
        public string UserId { get; set; }
        
        public ApplicationUser User { get; set; }
        
        public string JsonData { get; set; }
        
        public DateTime LastUpdated { get; set; }
    }
}

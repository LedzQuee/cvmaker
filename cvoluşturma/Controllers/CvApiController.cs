using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using cvoluşturma.Data;
using cvoluşturma.Models;

namespace cvoluşturma.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [Authorize]
    public class CvApiController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly UserManager<ApplicationUser> _userManager;

        public CvApiController(AppDbContext context, UserManager<ApplicationUser> userManager)
        {
            _context = context;
            _userManager = userManager;
        }

        [HttpGet("load")]
        public async Task<IActionResult> LoadCv()
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null) return Unauthorized();

            var cv = await _context.CvDocuments.FirstOrDefaultAsync(c => c.UserId == user.Id);
            if (cv == null) return Ok(new { success = false, message = "No CV found" });

            return Ok(new { success = true, data = cv.JsonData });
        }

        [HttpPost("save")]
        [RequestSizeLimit(1_000_000)] // Maks 1 MB - DoS Koruması
        public async Task<IActionResult> SaveCv([FromBody] System.Text.Json.JsonElement data)
        {
            var user = await _userManager.GetUserAsync(User);
            if (user == null) return Unauthorized();

            // JSON boyutu kontrolü
            var jsonString = data.GetRawText();
            if (jsonString.Length > 900_000)
                return BadRequest(new { success = false, message = "CV verisi çok büyük." });

            var cv = await _context.CvDocuments.FirstOrDefaultAsync(c => c.UserId == user.Id);
            if (cv == null)
            {
                cv = new CvDocument
                {
                    UserId = user.Id,
                    JsonData = jsonString,
                    LastUpdated = DateTime.UtcNow
                };
                _context.CvDocuments.Add(cv);
            }
            else
            {
                cv.JsonData = jsonString;
                cv.LastUpdated = DateTime.UtcNow;
                _context.CvDocuments.Update(cv);
            }

            await _context.SaveChangesAsync();
            return Ok(new { success = true });
        }
    }
}
